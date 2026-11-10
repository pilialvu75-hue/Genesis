"""Plain JSONL datasets with strict, dependency-free validation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_jsonl(path: str | Path, kind: str) -> list[dict]:
    if kind not in {"train", "eval"}:
        raise ValueError("kind must be train or eval")
    seen: set[str] = set()
    samples: list[dict] = []
    with Path(path).open("r", encoding="utf-8-sig") as file:
        for line_num, line in enumerate(file, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_num}: invalid JSON: {exc.msg}") from exc
            if not isinstance(record, dict):
                raise ValueError(f"{path}:{line_num}: each line must be a JSON object")
            for key in ("id", "prompt"):
                if not isinstance(record.get(key), str) or not record[key].strip():
                    raise ValueError(f"{path}:{line_num}: missing nonempty {key}")
            if record["id"] in seen:
                raise ValueError(f"{path}:{line_num}: duplicate id {record['id']!r}")
            seen.add(record["id"])
            if kind == "train":
                if not isinstance(record.get("response"), str) or not record["response"].strip():
                    raise ValueError(f"{path}:{line_num}: missing nonempty response")
            else:
                expected = record.get("expected")
                if isinstance(expected, str):
                    expected = [expected]
                if not isinstance(expected, list) or not expected or any(
                    not isinstance(value, str) or not value.strip() for value in expected
                ):
                    raise ValueError(f"{path}:{line_num}: expected must be a string or list of strings")
                record["expected"] = expected
            samples.append(record)
    if not samples:
        raise ValueError(f"{path}: no samples")
    return samples


def assert_no_overlap(train: list[dict], evaluation: list[dict]) -> None:
    train_ids = {sample["id"] for sample in train}
    eval_ids = {sample["id"] for sample in evaluation}
    duplicate_ids = train_ids & eval_ids
    if duplicate_ids:
        raise ValueError(f"training/evaluation IDs overlap: {sorted(duplicate_ids)}")
    train_prompts = {sample["prompt"].strip().casefold() for sample in train}
    eval_prompts = {sample["prompt"].strip().casefold() for sample in evaluation}
    if train_prompts & eval_prompts:
        raise ValueError("training/evaluation prompts overlap")
