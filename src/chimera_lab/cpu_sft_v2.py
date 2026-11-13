"""Zero-cost CPU SFT experiment v2 from verified public datasets.

A real LoRA training run, strictly a technical Chimera pilot. Never promote it
without larger independent evaluation or replace AIVEXUS models automatically.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
import math
import os
import random
import re
import statistics
import time
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path

BASE = "Qwen/Qwen3-0.6B"
DEFAULT_SEED = 241

def sha256_file(path: str | Path) -> str:
    sha = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            sha.update(block)
    return sha.hexdigest()

def plan_examples(examples: list[dict], steps: int, seed: int) -> list[dict]:
    """Interleave public-data sources and languages with a reproducible schedule.

    Single-task rows rotate without replacement within each source bucket.
    Avoid learning just mathematics because one math dataset is larger.
    """
    if steps < 1:
        raise ValueError("steps must be positive")
    rng = random.Random(seed)
    buckets = defaultdict(list)
    for sample in examples:
        key = (sample.get("source", "unknown"), sample.get("language", "en"))
        buckets[key].append(sample)
    if len(buckets) < 3:
        raise ValueError("At least three source/language groups required")
    keys = sorted(buckets)
    for key in keys:
        rng.shuffle(buckets[key])
    positions = dict.fromkeys(keys, 0)
    scheduled = []
    for index in range(steps):
        key = keys[index % len(keys)]
        current = buckets[key]
        pos = positions[key]
        if pos >= len(current):
            rng.shuffle(current)
            pos = 0
        scheduled.append(current[pos])
        positions[key] = pos + 1
    return scheduled

def numeric_match(text: str, expected: str) -> bool:
    """Best-effort arithmetic-only diagnostic: last numeric token."""
    from decimal import Decimal, InvalidOperation
    candidates = re.findall(r"(?<![\w])[-+]?\d[\d,]*(?:\.\d+)?(?![\w])", text)
    if not candidates:
        return False
    try:
        return Decimal(candidates[-1].replace(",", "")) == Decimal(expected)
    except InvalidOperation:
        return False

def run(args):
    import torch
    from peft import LoraConfig, PeftModel, get_peft_model
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if torch.cuda.is_available():
        raise RuntimeError("This workflow is intentionally CPU-only; run QLoRA on ASUS separately.")
    torch.manual_seed(args.seed)
    random.seed(args.seed)
    torch.set_num_threads(min(4, os.cpu_count() or 1))
    start = time.monotonic()
    train_path = Path(args.train)
    eval_path = Path(args.eval)
    target = Path(args.output)
    if target.exists() and any(target.iterdir()):
        raise FileExistsError(f"Refusing to overwrite existing weights: {target}")
    target.mkdir(parents=True, exist_ok=True)
    train = [json.loads(line) for line in train_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    tests = [json.loads(line) for line in eval_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    from .data import assert_no_overlap
    assert_no_overlap(train, [
        {"id": t["id"], "prompt": t["prompt"], "expected": t["expected"]}
        for t in tests
    ])
    if len(train) < 300 or len(tests) < 30:
        raise ValueError("Not enough independent real-world train/eval examples")
    if args.steps < 24:
        raise ValueError("At least 24 meaningful optimization steps expected")

    tokenizer = AutoTokenizer.from_pretrained(BASE, trust_remote_code=False)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        BASE, torch_dtype=torch.float32, trust_remote_code=False,
        low_cpu_mem_usage=True, device_map="cpu"
    )

    heldout = [
        ("it","Quanto fa 19 più 18? Rispondi solo con il numero.","37"),
        ("it","Calcola 8 × 13. Scrivi soltanto il risultato numerico.","104"),
        ("fr","Combien font 27 plus 16 ? Réponds uniquement par le nombre.","43"),
        ("fr","Calcule 12 multiplié par 8. Donne uniquement le résultat numérique.","96"),
        ("en","What is 23 plus 29? Reply with the number only.","52"),
        ("en","What is 14 times 6? Reply with the number only.","84"),
    ]
    normalized_train = {" ".join(t["prompt"].casefold().split()) for t in train}
    if any(" ".join(t[1].casefold().split()) in normalized_train for t in heldout):
        raise RuntimeError("Smoke-test prompt overlaps training prompts")

    def generate(model, prompt):
        model.eval()
        batch = tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}],
            tokenize=True, return_tensors="pt", return_dict=True,
            add_generation_prompt=True, enable_thinking=False,
        )
        with torch.inference_mode():
            output = model.generate(
                **batch, do_sample=False, max_new_tokens=48,
                pad_token_id=tokenizer.pad_token_id
            )
        return tokenizer.decode(output[0, batch["input_ids"].shape[-1]:],
                                skip_special_tokens=True).strip()

    baseline_answers = [generate(model, prompt) for _,prompt,_ in heldout]
    config = LoraConfig(
        r=8, lora_alpha=16, target_modules=["q_proj","v_proj"],
        lora_dropout=0.05, bias="none", task_type="CAUSAL_LM"
    )
    model = get_peft_model(model, config)
    trainable = [(name,param) for name,param in model.named_parameters() if param.requires_grad]
    if not trainable:
        raise RuntimeError("No trainable parameters")
    initial = {name:param.detach().clone() for name,param in trainable}

    def encode(example):
        user=[{"role":"user", "content":example["prompt"]}]
        messages=user+[{"role":"assistant","content":example["response"]}]
        prefix=tokenizer.apply_chat_template(user, tokenize=True, add_generation_prompt=True)
        complete=tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=False)
        if complete[:len(prefix)] != prefix:
            return None
        if len(prefix) > args.max_length - 24:
            return None
        tokens=complete[:args.max_length]
        labels=[-100]*len(prefix)+tokens[len(prefix):]
        if sum(x!=-100 for x in labels)<8:
            return None
        return (
            torch.tensor([tokens],dtype=torch.long),
            torch.tensor([labels],dtype=torch.long),
            torch.ones((1,len(tokens)),dtype=torch.long),
        )

    encoded = []
    sources = Counter()
    skipped = Counter()
    for row in train:
        sample = encode(row)
        if sample is None:
            skipped[row["source"]] += 1
        else:
            encoded.append((row, sample))
            sources[row["source"]] += 1
    if len(encoded) < 200:
        raise RuntimeError(f"Only {len(encoded)} samples survived length and template checks")
    schedule = plan_examples([row for row,_ in encoded], args.steps, args.seed)
    by_id={row["id"]:sample for row,sample in encoded}
    optimizer=torch.optim.AdamW([p for _,p in trainable], lr=args.learning_rate,
                                 weight_decay=0.01)
    losses=[]
    seen_ids=set()
    model.train()
    for i,row in enumerate(schedule):
        model.train()
        scale=0.1+0.9*min(1.0,(i+1)/max(1,args.warmup_steps))
        scale*=0.5*(1+math.cos(math.pi*i/args.steps))
        optimizer.param_groups[0]["lr"]=args.learning_rate*scale
        input_ids, labels, attention = by_id[row["id"]]
        optimizer.zero_grad(set_to_none=True)
        result=model(input_ids=input_ids, labels=labels,
                     attention_mask=attention, use_cache=False)
        loss=result.loss
        if not torch.isfinite(loss):
            raise RuntimeError(f"Nonfinite loss at step {i+1}")
        loss.backward()
        torch.nn.utils.clip_grad_norm_([p for _,p in trainable], max_norm=1.0)
        optimizer.step()
        losses.append(float(loss.detach()))
        seen_ids.add(row["id"])
        if (i+1)%20==0 or i==0:
            print(f"SFT step {i+1}/{args.steps}, loss={losses[-1]:.4f}, "
                  f"unique_rows={len(seen_ids)}, elapsed={time.monotonic()-start:.0f}s",
                  flush=True)

    changed=sum(float((p.detach()-initial[name]).abs().sum()) for name,p in trainable)
    if changed <= 0.0:
        raise RuntimeError("Weights did not change; abort")
    model.eval()
    trained_answers=[generate(model, prompt) for _,prompt,_ in heldout]
    model.save_pretrained(target, safe_serialization=True)
    tokenizer.save_pretrained(target)
    weights=target/"adapter_model.safetensors"
    if not weights.is_file() or weights.stat().st_size<1000:
        raise RuntimeError("No real trained weights saved")

    # Strong technical gate: use a separate PEFT model loaded from disk, not
    # the in-memory trained object, before declaring inference successful.
    del model, optimizer, trainable, initial
    gc.collect()
    reloaded_base=AutoModelForCausalLM.from_pretrained(
        BASE, torch_dtype=torch.float32, trust_remote_code=False,
        low_cpu_mem_usage=True, device_map="cpu"
    )
    reloaded=PeftModel.from_pretrained(reloaded_base,str(target))
    verification=[generate(reloaded,prompt) for _,prompt,_ in heldout]
    if trained_answers!=verification:
        raise RuntimeError("Reloaded candidate differs from in-memory candidate")

    results=[]
    for (lang,prompt,expected),old,new in zip(heldout,baseline_answers,trained_answers):
        results.append({
            "language":lang,"prompt":prompt,"expected":expected,
            "baseline":old,"candidate":new,
            "baseline_correct":numeric_match(old,expected),
            "candidate_correct":numeric_match(new,expected)
        })
    report={
        "schema":"chimera.cpu-real-sft.v2",
        "status":"TECHNICAL_PILOT_NOT_FINAL_CHIMERA1",
        "base":BASE,
        "data_sources":dict(sources),
        "training_examples_available":len(encoded),
        "unique_examples_used":len(seen_ids),
        "training_steps":args.steps,
        "max_length":args.max_length,
        "learning_rate":args.learning_rate,
        "seed":args.seed,
        "schedule":"source-and-language balanced, shuffled per bucket",
        "skipped_too_long_or_bad_template":dict(skipped),
        "train_sha256":sha256_file(train_path),
        "held_out_math_sha256":sha256_file(eval_path),
        "adapter_sha256":sha256_file(weights),
        "weight_change_l1":round(changed,4),
        "loss_first20_mean":round(statistics.mean(losses[:20]),5),
        "loss_last20_mean":round(statistics.mean(losses[-20:]),5),
        "check_reloaded_inference":True,
        "pilot_arithmetic_results":results,
        "pilot_arithmetic_baseline_correct":sum(r["baseline_correct"] for r in results),
        "pilot_arithmetic_candidate_correct":sum(r["candidate_correct"] for r in results),
        "duration_seconds":round(time.monotonic()-start,2),
        "completed_utc":datetime.now(timezone.utc).isoformat(),
        "warning":"Only 6 untrained-on arithmetic diagnostics; no broad quality claim. "
                  "This is Qwen3-0.6B with a LoRA adapter, not the targeted Chimera 1."
    }
    (target/"report.json").write_text(
        json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],"train_count":len(encoded),
       "training_steps":args.steps,
       "adapter_sha256":report["adapter_sha256"],
       "base_correct":report["pilot_arithmetic_baseline_correct"],
       "trained_correct":report["pilot_arithmetic_candidate_correct"],
       "duration_seconds":report["duration_seconds"]},indent=2),flush=True)

def main(argv=None):
    p=argparse.ArgumentParser(description="Zero-cost substantial CPU LoRA pilot")
    p.add_argument("--train",default="data/chimera1_train.jsonl")
    p.add_argument("--eval",default="data/chimera1_math_eval.jsonl")
    p.add_argument("--output",default="outputs/chimera1_cpu_real_sft_v2")
    p.add_argument("--steps",type=int,default=240)
    p.add_argument("--max-length",type=int,default=192)
    p.add_argument("--seed",type=int,default=DEFAULT_SEED)
    p.add_argument("--learning-rate",type=float,default=0.00018)
    p.add_argument("--warmup-steps",type=int,default=18)
    args=p.parse_args(argv)
    if args.max_length<96 or args.learning_rate<=0 or args.warmup_steps<0:
        p.error("Invalid hyperparameters")
    run(args)

if __name__=="__main__":
    main()
