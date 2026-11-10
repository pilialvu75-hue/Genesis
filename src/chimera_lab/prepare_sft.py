"""Prepare Chimera 1 training examples from permissively licensed upstream datasets.

Downloads only when explicitly run. No datasets or private data bundled in Git.
"""
from __future__ import annotations

import argparse
import hashlib
import heapq
import json
import re
from pathlib import Path

SOURCES = {
    "aya": ("CohereLabs/aya_dataset", "Apache-2.0"),
    "oasst": ("OpenAssistant/oasst1", "Apache-2.0"),
    "gsm8k": ("openai/gsm8k", "MIT"),
    "metamath": ("meta-math/MetaMathQA", "MIT"),
}

def clean(value: object) -> str:
    return " ".join(value.strip().split()) if isinstance(value, str) else ""

def digest(value: str) -> str:
    return hashlib.sha256(clean(value).casefold().encode("utf-8")).hexdigest()

def select(rows, count: int) -> list[dict]:
    """Order-independent deterministic hash sampling with prompt deduplication."""
    heap, seen = [], set()
    for index, row in enumerate(rows):
        if not row:
            continue
        prompt, response = clean(row.get("prompt")), clean(row.get("response"))
        if not (12 <= len(prompt) <= 12000 and 12 <= len(response) <= 20000):
            continue
        key = digest(prompt)
        if key in seen:
            continue
        seen.add(key)
        entry = (-int(key[:16], 16), index, {**row, "prompt": prompt, "response": response})
        if len(heap) < count:
            heapq.heappush(heap, entry)
        elif entry[0] > heap[0][0]:
            heapq.heapreplace(heap, entry)
    return [x[2] for x in sorted(heap, key=lambda x: -x[0])]

def aya_rows(rows, language: str):
    for row in rows:
        if row.get("language_code") != language:
            continue
        if row.get("annotation_type") not in (None, "original-annotations", "original_annotations"):
            continue
        yield {"prompt": row.get("inputs"), "response": row.get("targets"),
               "language": language, "source": "aya"}

def gsm_rows(rows):
    for row in rows:
        answer = row.get("answer")
        if not isinstance(answer, str) or "####" not in answer:
            continue
        steps, final = answer.rsplit("####", 1)
        steps = re.sub(r"<<[^>]*>>", "", steps).strip()
        yield {"prompt": row.get("question"),
               "response": f"{steps}\nAnswer: {final.strip()}",
               "language": "en", "source": "gsm8k"}

def metamath_rows(rows):
    for row in rows:
        # MATH-only avoids accidentally mixing GSM8K training questions twice.
        if str(row.get("type", "")).startswith("MATH_"):
            yield {"prompt": row.get("query"), "response": row.get("response"),
                   "language": "en", "source": "metamath"}

def oasst_rows(rows, language: str):
    messages = list(rows)
    parents = {row.get("message_id"): row for row in messages if row.get("role") == "prompter"}
    for row in messages:
        if row.get("role") != "assistant" or row.get("lang") != language:
            continue
        if row.get("deleted") or row.get("synthetic") or row.get("review_result") is not True:
            continue
        if row.get("rank") not in (None, 0):
            continue
        parent = parents.get(row.get("parent_id"))
        if not parent or parent.get("deleted") or parent.get("parent_id") is not None:
            continue
        if parent.get("lang") == language:
            yield {"prompt": parent.get("text"), "response": row.get("text"),
                   "language": language, "source": "oasst"}

def math_holdout(rows, limit: int) -> list[dict]:
    examples = []
    for row in rows:
        question, answer = clean(row.get("question")), row.get("answer")
        if not question or not isinstance(answer, str) or "####" not in answer:
            continue
        number = answer.rsplit("####", 1)[1].strip().replace(",", "")
        if not re.fullmatch(r"-?\d+(?:\.\d+)?", number):
            continue
        examples.append({
            "id": "gsm8k-test-" + digest(question)[:24],
            "prompt": question + "\nSolve carefully. End with a separate line: Answer: <number>",
            "expected": [number], "scoring": "final_number",
        })
    return sorted(examples, key=lambda row: digest(row["prompt"]))[:limit]

def write_jsonl(path: Path, rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        for row in rows:
            file.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")

def build(train_output: Path, eval_output: Path, per_lang: int,
          math_count: int, dialogue_count: int, metamath_count: int, eval_count: int):
    from datasets import load_dataset
    from .data import assert_no_overlap, read_jsonl, sha256_file

    collected, counts = [], {}
    aya = load_dataset("CohereLabs/aya_dataset", split="train", streaming=True)
    for language in ("ita", "fra", "eng"):
        chunk = select(aya_rows(aya, language), per_lang)
        counts["aya_" + language] = len(chunk)
        collected.extend(chunk)
    oasst = load_dataset("OpenAssistant/oasst1", split="train", streaming=True)
    for language in ("it", "fr", "en"):
        chunk = select(oasst_rows(oasst, language), dialogue_count)
        counts["oasst_" + language] = len(chunk)
        collected.extend(chunk)
    gsm8k = load_dataset("openai/gsm8k", "main", split="train", streaming=True)
    chunk = select(gsm_rows(gsm8k), math_count)
    counts["gsm8k_train"] = len(chunk)
    collected.extend(chunk)
    metamath = load_dataset("meta-math/MetaMathQA", split="train", streaming=True)
    chunk = select(metamath_rows(metamath), metamath_count)
    counts["metamath_train"] = len(chunk)
    collected.extend(chunk)

    unique = {}
    for row in collected:
        unique.setdefault(digest(row["prompt"]), row)
    train = sorted(
        ({**row, "id": row["source"] + "-" + digest(row["prompt"])[:24]}
         for row in unique.values()), key=lambda row: digest(row["prompt"])
    )
    eval_rows = math_holdout(
        load_dataset("openai/gsm8k", "main", split="test", streaming=True), eval_count
    )
    if not train or not eval_rows:
        raise RuntimeError("Empty training or evaluation set")
    write_jsonl(train_output, train)
    write_jsonl(eval_output, eval_rows)
    assert_no_overlap(read_jsonl(train_output, "train"), read_jsonl(eval_output, "eval"))
    manifest = {
        "schema": "chimera.data.v1",
        "sampling": "SHA256(prompt), fixed quotas, deduplicate prompts",
        "sources": {k: {"repo": v[0], "declared_license": v[1]} for k,v in SOURCES.items()},
        "counts_before_dedup": counts,
        "train_examples": len(train), "held_out_math_examples": len(eval_rows),
        "train_sha256": sha256_file(train_output),
        "eval_sha256": sha256_file(eval_output),
        "note": "Recheck upstream licenses and inspect quality before distribution; GSM8K test stays out of training.",
    }
    train_output.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return manifest

def main(argv=None):
    parser = argparse.ArgumentParser(description="Build multilingual Chimera 1 SFT data")
    parser.add_argument("--train-output", default="data/chimera1_train.jsonl")
    parser.add_argument("--eval-output", default="data/chimera1_math_eval.jsonl")
    parser.add_argument("--per-lang", type=int, default=2000)
    parser.add_argument("--math-count", type=int, default=5000)
    parser.add_argument("--dialogue-count", type=int, default=700)
    parser.add_argument("--metamath-count", type=int, default=2000)
    parser.add_argument("--eval-count", type=int, default=500)
    args = parser.parse_args(argv)
    if min(args.per_lang, args.math_count, args.dialogue_count,
           args.metamath_count, args.eval_count) < 1:
        parser.error("All quotas must be positive")
    report = build(Path(args.train_output), Path(args.eval_output),
                   args.per_lang, args.math_count, args.dialogue_count,
                   args.metamath_count, args.eval_count)
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
