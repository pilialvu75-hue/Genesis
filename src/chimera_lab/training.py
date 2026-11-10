"""Minimal genuine QLoRA experiment. No synthetic success claims."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .data import assert_no_overlap, read_jsonl, sha256_file
from .metrics import write_json


def encode_training_samples(samples: list[dict], tokenizer, max_length: int) -> list[dict]:
    """Mask instruction tokens; train on assistant response only."""
    encoded = []
    for sample in samples:
        user = [{"role": "user", "content": sample["prompt"]}]
        both = user + [{"role": "assistant", "content": sample["response"]}]
        prefix = tokenizer.apply_chat_template(user, tokenize=True, add_generation_prompt=True)
        full = tokenizer.apply_chat_template(both, tokenize=True, add_generation_prompt=False)
        if full[:len(prefix)] != prefix:
            raise ValueError(f"chat template prefix mismatch for {sample['id']}")
        if len(prefix) >= max_length:
            raise ValueError(f"prompt too long for {sample['id']} at max_length {max_length}")
        shortened = full[:max_length]
        if len(shortened) <= len(prefix):
            raise ValueError(f"no response tokens for {sample['id']}")
        labels = [-100] * len(prefix) + shortened[len(prefix):]
        encoded.append({"input_ids": shortened, "labels": labels, "attention_mask": [1]*len(shortened)})
    return encoded


class PaddedDataset:
    def __init__(self, encoded: list[dict]):
        self.items = encoded

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]


def collator(features: list[dict], pad_token_id: int):
    import torch
    longest = max(len(row["input_ids"]) for row in features)
    keys = ("input_ids", "labels", "attention_mask")
    pad_values = {"input_ids": pad_token_id, "labels": -100, "attention_mask": 0}
    return {
        key: torch.tensor([row[key] + [pad_values[key]] * (longest - len(row[key]))
                           for row in features], dtype=torch.long)
        for key in keys
    }


def train_adapter(model_id: str, train_file: str, eval_file: str, output: str,
                  steps: int, max_length: int, learning_rate: float) -> dict:
    import torch
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    from transformers import Trainer, TrainingArguments

    from .engine import load_model

    if not torch.cuda.is_available():
        raise RuntimeError("First Chimera training protocol requires NVIDIA CUDA. No CPU/cloud fallback is silently used.")
    if steps < 1 or max_length < 64 or learning_rate <= 0:
        raise ValueError("steps>=1, max_length>=64 and learning_rate>0 required")
    samples = read_jsonl(train_file, "train")
    eval_samples = read_jsonl(eval_file, "eval")
    assert_no_overlap(samples, eval_samples)
    if Path(output).exists() and any(Path(output).iterdir()):
        raise FileExistsError("Output directory must be empty: protect previous checkpoints")
    model, tokenizer, _ = load_model(model_id, "4bit")
    model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=True)
    config = LoraConfig(
        r=8, lora_alpha=16, target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05, bias="none", task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, config)
    model.config.use_cache = False
    encoded = encode_training_samples(samples, tokenizer, max_length)
    args = TrainingArguments(
        output_dir=str(Path(output) / "trainer"), max_steps=steps,
        per_device_train_batch_size=1, gradient_accumulation_steps=4,
        learning_rate=learning_rate, logging_steps=1,
        save_strategy="no", report_to="none", remove_unused_columns=False,
        fp16=True, optim="paged_adamw_8bit", dataloader_num_workers=0,
        seed=42,
    )
    trainer = Trainer(
        model=model, args=args, train_dataset=PaddedDataset(encoded),
        data_collator=lambda items: collator(items, tokenizer.pad_token_id),
    )
    trainer.train()
    target = Path(output)
    target.mkdir(parents=True, exist_ok=True)
    # A PEFT model's save_pretrained saves genuinely trained LoRA adapter weights.
    trainer.model.save_pretrained(target, safe_serialization=True)
    tokenizer.save_pretrained(target)
    manifest = {
        "kind": "chimera.qlora.adapter.v1", "name": "Chimera 1 experiment",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "base_model": model_id, "train_file_sha256": sha256_file(train_file),
        "held_out_eval_sha256": sha256_file(eval_file),
        "train_examples": len(samples), "train_steps": steps,
        "max_length": max_length, "learning_rate": learning_rate,
        "lora": {"r": 8, "alpha": 16, "targets": ["q_proj", "v_proj"]},
        "torch_version": torch.__version__,
        "device": torch.cuda.get_device_name(0),
        "note": "Adapter is a real weight modification, but is NOT a wholly new pretrained foundation model.",
    }
    write_json(target / "chimera_manifest.json", manifest)
    return manifest
