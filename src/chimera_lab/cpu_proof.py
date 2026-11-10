"""Train and verify a real, *small* CPU-only LoRA proof, not final Chimera 1.

Outputs a Hugging Face PEFT adapter artifact. The workflow runs only on a public
GitHub repository's standard free CPU runner. No secrets or paid inference.
"""
from __future__ import annotations

import gc
import hashlib
import json
import os
import random
import time
from datetime import datetime, timezone
from pathlib import Path

BASE_ID = "Qwen/Qwen3-0.6B"


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main():
    import torch
    from peft import LoraConfig, PeftModel, get_peft_model
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch.set_num_threads(min(4, os.cpu_count() or 1))
    torch.manual_seed(147)
    random.seed(147)
    assert not torch.cuda.is_available(), "This experiment is intentionally CPU-only"
    data_path = Path("data/chimera1_cpu_proof_train.jsonl")
    examples = [json.loads(line) for line in data_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(examples) >= 12
    target = Path("outputs/chimera1_cpu_proof")
    target.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()

    tokenizer = AutoTokenizer.from_pretrained(BASE_ID, trust_remote_code=False)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token

    def load_base():
        return AutoModelForCausalLM.from_pretrained(
            BASE_ID, torch_dtype=torch.float32, trust_remote_code=False,
            low_cpu_mem_usage=True, device_map="cpu"
        )

    def generate(model, prompt):
        model.eval()
        # Qwen3 supports disabling thinking mode in the chat template.
        batch = tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}],
            tokenize=True, return_dict=True, return_tensors="pt",
            add_generation_prompt=True, enable_thinking=False,
        )
        with torch.inference_mode():
            output = model.generate(
                **batch, max_new_tokens=28, do_sample=False,
                pad_token_id=tokenizer.pad_token_id,
            )
        new_ids = output[0, batch["input_ids"].size(1):]
        return tokenizer.decode(new_ids, skip_special_tokens=True).strip()

    model = load_base()
    eval_prompts = [
        "In italiano: a cosa servono i test separati dall'addestramento?",
        "En français : pourquoi faut-il conserver une version de référence ?",
        "In English: explain why reproducible evaluation matters.",
    ]
    baseline = [generate(model, q) for q in eval_prompts]
    config = LoraConfig(
        r=8, lora_alpha=16, target_modules=["q_proj", "v_proj"],
        lora_dropout=0.0, bias="none", task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, config)
    trainable = [(name, p) for name,p in model.named_parameters() if p.requires_grad]
    assert trainable, "No trainable LoRA parameters"
    initial = {name: param.detach().clone() for name,param in trainable}

    def encode(example):
        user = [{"role": "user", "content": example["prompt"]}]
        complete = user + [{"role": "assistant", "content": example["response"]}]
        prefix = tokenizer.apply_chat_template(user, tokenize=True, add_generation_prompt=True)
        full = tokenizer.apply_chat_template(complete, tokenize=True, add_generation_prompt=False)
        if full[:len(prefix)] != prefix:
            raise ValueError("Chat template prefix mismatch; refusing to train incorrect labels")
        if len(full) > 160:
            raise ValueError("Example exceeds context length")
        labels = [-100] * len(prefix) + full[len(prefix):]
        return (torch.tensor([full]), torch.tensor([labels]), torch.ones(1, len(full),dtype=torch.long))

    encoded = [encode(row) for row in examples]
    optimizer = torch.optim.AdamW([p for _,p in trainable], lr=0.0003)
    losses=[]
    model.train()
    for step in range(12):
        ids, labels, attention = encoded[(step * 7) % len(encoded)]
        optimizer.zero_grad(set_to_none=True)
        output = model(input_ids=ids, labels=labels, attention_mask=attention, use_cache=False)
        loss = output.loss
        if not torch.isfinite(loss):
            raise RuntimeError(f"Non-finite training loss at {step}")
        loss.backward()
        optimizer.step()
        losses.append(round(float(loss.detach()), 7))
        print(f"train step {step+1}/12 loss={losses[-1]}", flush=True)

    changed = sum(
        float((param.detach() - initial[name]).abs().sum())
        for name,param in trainable
    )
    if not changed > 0:
        raise RuntimeError("Adapter weights did not change! Refusing success.")
    model.eval()
    trained = [generate(model, q) for q in eval_prompts]
    model.save_pretrained(target, safe_serialization=True)
    tokenizer.save_pretrained(target)
    weights=target/"adapter_model.safetensors"
    if not weights.exists() or weights.stat().st_size < 1000:
        raise RuntimeError("No actual LoRA adapter weights saved")

    del model, optimizer, trainable, initial
    gc.collect()
    loaded = PeftModel.from_pretrained(load_base(), str(target))
    reloaded = [generate(loaded, q) for q in eval_prompts]
    if trained != reloaded:
        raise RuntimeError("Reloaded LoRA model generated different results: inference check failed")

    report = {
        "schema": "chimera.cpu-pilot.v1",
        "status": "PILOT_ONLY_NOT_FINAL_CHIMERA1",
        "base_model": BASE_ID,
        "base_license": "Apache-2.0",
        "trained_adapter_sha256": sha256(weights),
        "training_data_sha256": sha256(data_path),
        "train_count": len(examples),
        "steps": len(losses),
        "losses": losses,
        "absolute_weight_change": round(changed, 6),
        "trainable_parameter_count": sum(p.numel() for p in loaded.parameters() if p.requires_grad),
        "checkpoint_reloaded_and_inference_verified": True,
        "probe_prompts": eval_prompts,
        "baseline_responses": baseline,
        "trained_responses": trained,
        "reloaded_responses": reloaded,
        "duration_seconds": round(time.monotonic() - started, 2),
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "warning": "Engineering smoke test on a 0.6B model with 24 original examples. It is not an intelligence improvement claim, not the targeted 4B model, and not ready for public AIVEXUS distribution.",
    }
    (target/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({key:report[key] for key in (
        "status","base_model","trained_adapter_sha256",
        "checkpoint_reloaded_and_inference_verified","duration_seconds")},indent=2),flush=True)


if __name__ == "__main__":
    main()
