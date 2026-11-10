"""Run actual inference and record per-question latency and correctness."""

from __future__ import annotations

import time
from datetime import datetime, timezone

from .data import read_jsonl, sha256_file
from .engine import load_model, predict
from .metrics import matches_expected, matches_final_number, summarise, write_json


def evaluate(source: str, eval_file: str, output: str, quantization: str, max_new_tokens: int) -> dict:
    examples = read_jsonl(eval_file, "eval")
    model, tokenizer, base_id = load_model(source, quantization)
    rows = []
    for sample in examples:
        started = time.perf_counter()
        row = {"id": sample["id"], "expected": sample["expected"]}
        try:
            response, generated = predict(model, tokenizer, sample["prompt"], max_new_tokens)
            row.update({"response": response, "new_tokens": generated,
                        "correct": matches_final_number(response, sample["expected"]) if sample.get("scoring") == "final_number" else matches_expected(response, sample["expected"])})
        except (RuntimeError, ValueError) as exc:
            row.update({"error": f"{type(exc).__name__}: {exc}", "correct": None})
        row["seconds"] = round(time.perf_counter() - started, 4)
        rows.append(row)
    report = {
        "schema": "chimera.eval.v1", "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "model": source, "base_model": base_id, "quantization": quantization,
        "eval_sha256": sha256_file(eval_file),
        "generation": {"max_new_tokens": max_new_tokens, "do_sample": False},
        "metrics": summarise(rows), "samples": rows,
        "disclaimer": "Diagnostic final-answer/exact-match only; NOT evidence of general intelligence or model superiority.",
    }
    write_json(output, report)
    return report
