"""Run unmodified Qwen and the Chimera LoRA pilot under identical llama.cpp settings.

A tiny held-out diagnostic, NOT a comprehensive benchmark of model quality.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1048576), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_answer(log: str, prompt: str) -> str:
    marker = "> " + prompt
    start = log.find(marker)
    if start == -1:
        raise ValueError("Expected echoed prompt not found in llama-cli output")
    response = log[start + len(marker):]
    for delimiter in ("common_memory_breakdown_print:", "\n[ Prompt:", "\nExiting..."):
        response = response.split(delimiter, 1)[0]
    return response.strip()


def numeric_score(answer: str, expected: str) -> bool:
    """Heuristic for small arithmetic tests: look at last displayed number."""
    numbers = re.findall(r"(?<![\w])[-+]?\d[\d,]*(?:\.\d+)?(?![\w])", answer)
    if not numbers:
        return False
    from decimal import Decimal, InvalidOperation
    try:
        return Decimal(numbers[-1].replace(",", "")) == Decimal(expected)
    except InvalidOperation:
        return False


def inference(binary: str, path: str, prompt: str, timeout: int) -> tuple[str, float]:
    argv = [
        binary, "-m", path, "-p", prompt, "-n", "64", "-c", "1024",
        "-t", "4", "--temp", "0", "--single-turn", "--simple-io",
    ]
    start = time.perf_counter()
    result = subprocess.run(argv, input="", text=True, capture_output=True, timeout=timeout)
    elapsed = round(time.perf_counter() - start, 3)
    full_log = result.stdout + result.stderr
    if result.returncode != 0:
        raise RuntimeError(f"llama-cli failed with exit code {result.returncode}: {full_log[-1000:]}")
    response = extract_answer(full_log, prompt)
    if not response:
        raise RuntimeError("Empty model response")
    return response, elapsed


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--binary", required=True)
    p.add_argument("--base", required=True)
    p.add_argument("--candidate", required=True)
    p.add_argument("--dataset", default="data/chimera1_holdout_smoke.jsonl")
    p.add_argument("--out", default="outputs/chimera1_base_vs_pilot.json")
    p.add_argument("--timeout", type=int, default=45)
    args = p.parse_args()
    data_path = Path(args.dataset)
    rows = [json.loads(line) for line in data_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(rows) >= 12
    answers = {}
    for name, model in [("base", args.base), ("candidate", args.candidate)]:
        answers[name] = []
        for item in rows:
            print(f"[{name}] {item['id']} {item['language']}", flush=True)
            try:
                response, duration = inference(args.binary, model, item["prompt"], args.timeout)
                scored = numeric_score(response, item["expected_number"]) if item.get("expected_number") else None
                answers[name].append({
                    "id": item["id"], "language": item["language"], "response": response,
                    "numeric_correct": scored, "elapsed_seconds": duration,
                })
                print(f"  done in {duration}s; numeric_correct={scored}", flush=True)
            except (subprocess.TimeoutExpired, RuntimeError, ValueError) as error:
                answers[name].append({
                    "id": item["id"], "language": item["language"],
                    "error": f"{type(error).__name__}: {error}", "numeric_correct": None,
                })
                print(f"  ERROR {error}", flush=True)

    def totals(items):
        numeric = [x for x in items if x["id"] in {
            y["id"] for y in rows if "expected_number" in y
        }]
        return {
            "numeric_correct": sum(x.get("numeric_correct") is True for x in numeric),
            "numeric_total": len(numeric),
            "errors": sum(bool(x.get("error")) for x in items),
            "median_elapsed_seconds": __import__("statistics").median(
                x["elapsed_seconds"] for x in items if "elapsed_seconds" in x
            ) if any("elapsed_seconds" in x for x in items) else None,
        }

    report = {
        "schema": "chimera.baseline-heldout.v1",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "description": "Tiny held-out diagnostic: base vs real trained LoRA merged+Q4 pilot, same GGUF quantization, same llama.cpp revision.",
        "eval_sha256": sha256(data_path),
        "base_sha256": sha256(Path(args.base)),
        "candidate_sha256": sha256(Path(args.candidate)),
        "generation": {"max_new_tokens": 64, "context": 1024, "threads": 4, "temperature": 0, "single_turn": True},
        "base": answers["base"],
        "candidate": answers["candidate"],
        "base_summary": totals(answers["base"]),
        "candidate_summary": totals(answers["candidate"]),
        "note": "Nine short arithmetic prompts use a simple numeric heuristic; three open-ended prompts require manual review. No claim of general improvement or readiness.",
    }
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps({"base": report["base_summary"], "candidate": report["candidate_summary"]}, indent=2), flush=True)
    if report["base_summary"]["errors"] or report["candidate_summary"]["errors"]:
        raise RuntimeError("Some inference calls failed; report saved for diagnosis and must not be treated as valid benchmark")

if __name__ == "__main__":
    main()
