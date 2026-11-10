"""Deterministic diagnostics; NOT a comprehensive intelligence benchmark."""

from __future__ import annotations

import json
import re
import statistics
from pathlib import Path


def normalise(text: str) -> str:
    return " ".join(re.sub(r"[^\w\s]", " ", text.casefold(), flags=re.UNICODE).split())


def matches_expected(response: str, expected: list[str]) -> bool:
    return any(normalise(response) == normalise(choice) for choice in expected)


def summarise(rows: list[dict]) -> dict:
    good = [row for row in rows if not row.get("error")]
    scored = [row for row in good if row.get("correct") is not None]
    times = [row["seconds"] for row in good if isinstance(row.get("seconds"), (float, int))]
    gen_tokens = sum(row.get("new_tokens", 0) for row in good)
    wall = sum(times)
    return {
        "total": len(rows),
        "completed": len(good),
        "errors": len(rows) - len(good),
        "exact_match": (sum(bool(row["correct"]) for row in scored) / len(scored)) if scored else None,
        "median_latency_s": statistics.median(times) if times else None,
        "aggregate_tokens_per_s": (gen_tokens / wall) if wall else None,
    }


def compare_reports(baseline: dict, candidate: dict) -> dict:
    required = ("eval_sha256", "generation", "samples")
    for field in required:
        if baseline.get(field) is None or candidate.get(field) is None:
            raise ValueError(f"both reports must contain {field}")
    if baseline["eval_sha256"] != candidate["eval_sha256"]:
        raise ValueError("different evaluation datasets: comparison refused")
    if baseline["generation"] != candidate["generation"]:
        raise ValueError("different decoding parameters: comparison refused")
    base_ids = [x["id"] for x in baseline["samples"]]
    cand_ids = [x["id"] for x in candidate["samples"]]
    if base_ids != cand_ids:
        raise ValueError("evaluation IDs/order differ: comparison refused")
    a, b = summarise(baseline["samples"]), summarise(candidate["samples"])
    return {
        "baseline": baseline.get("model"),
        "candidate": candidate.get("model"),
        "eval_sha256": baseline["eval_sha256"],
        "baseline_metrics": a,
        "candidate_metrics": b,
        "delta_exact_match": (
            b["exact_match"] - a["exact_match"]
            if a["exact_match"] is not None and b["exact_match"] is not None else None
        ),
        "promotion": "NOT_AUTOMATIC: tiny exact-match diagnostics never prove general superiority",
    }


def write_json(path: str | Path, payload: dict) -> None:
    location = Path(path)
    location.parent.mkdir(parents=True, exist_ok=True)
    location.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
