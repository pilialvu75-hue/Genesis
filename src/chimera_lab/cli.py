"""Minimal Windows/Linux command line for Chimera 1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import DEFAULT_MODEL
from .data import assert_no_overlap, read_jsonl
from .device import doctor
from .metrics import compare_reports, write_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="chimera", description="Chimera 1 genuine experiment laboratory")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="Report machine and CUDA availability, without downloads")
    validate = sub.add_parser("validate-data", help="Validate examples and check train/eval leakage")
    validate.add_argument("--train-file", default="data/train_demo.jsonl")
    validate.add_argument("--eval-file", default="data/eval_demo.jsonl")
    baseline = sub.add_parser("evaluate", help="Evaluate real model inference (weights downloaded on first use)")
    baseline.add_argument("--model", default=DEFAULT_MODEL)
    baseline.add_argument("--eval-file", default="data/eval_demo.jsonl")
    baseline.add_argument("--output", required=True)
    baseline.add_argument("--quantization", choices=("4bit", "none"), default="4bit")
    baseline.add_argument("--max-new-tokens", type=int, default=96)
    train = sub.add_parser("train", help="Run actual 4-bit LoRA training and save adapter weights")
    train.add_argument("--model", default=DEFAULT_MODEL)
    train.add_argument("--train-file", default="data/train_demo.jsonl")
    train.add_argument("--eval-file", default="data/eval_demo.jsonl")
    train.add_argument("--output", required=True)
    train.add_argument("--steps", type=int, default=8)
    train.add_argument("--max-length", type=int, default=256)
    train.add_argument("--learning-rate", type=float, default=0.00015)
    compare = sub.add_parser("compare", help="Compare evaluation reports for same dataset/settings")
    compare.add_argument("--baseline", required=True)
    compare.add_argument("--candidate", required=True)
    compare.add_argument("--output", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "doctor":
        print(json.dumps(doctor(), indent=2, ensure_ascii=False))
    elif args.command == "validate-data":
        tr = read_jsonl(args.train_file, "train")
        ev = read_jsonl(args.eval_file, "eval")
        assert_no_overlap(tr, ev)
        print(json.dumps({"train": len(tr), "eval": len(ev), "status": "valid"}, indent=2))
    elif args.command == "evaluate":
        if args.max_new_tokens < 1:
            raise ValueError("max-new-tokens must be positive")
        from .evaluation import evaluate
        report = evaluate(args.model, args.eval_file, args.output,
                          args.quantization, args.max_new_tokens)
        print(json.dumps(report["metrics"], indent=2))
    elif args.command == "train":
        from .training import train_adapter
        manifest = train_adapter(args.model, args.train_file, args.eval_file,
                                 args.output, args.steps, args.max_length, args.learning_rate)
        print(json.dumps(manifest, indent=2))
    elif args.command == "compare":
        base = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
        cand = json.loads(Path(args.candidate).read_text(encoding="utf-8"))
        result = compare_reports(base, cand)
        write_json(args.output, result)
        print(json.dumps(result, indent=2))
    return 0
