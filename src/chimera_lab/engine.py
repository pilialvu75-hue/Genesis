"""Model loading and reproducible generation. Imports heavy dependencies lazily."""

from __future__ import annotations

import json
from pathlib import Path


def resolve_model(source: str) -> tuple[str, str | None]:
    """Return HF base ID, adapter path. Only local adapters produced by the lab."""
    root = Path(source)
    adapter = root / "adapter_config.json"
    if not adapter.is_file():
        return source, None
    cfg = json.loads(adapter.read_text(encoding="utf-8"))
    base_id = cfg.get("base_model_name_or_path")
    if not isinstance(base_id, str) or not base_id:
        raise ValueError("adapter has no base_model_name_or_path")
    return base_id, str(root)


def load_model(source: str, quantization: str):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

    if quantization not in {"4bit", "none"}:
        raise ValueError("quantization must be 4bit or none")
    base_id, adapter_path = resolve_model(source)
    tokenizer = AutoTokenizer.from_pretrained(base_id, trust_remote_code=False)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    args = {"trust_remote_code": False}
    if quantization == "4bit":
        if not torch.cuda.is_available():
            raise RuntimeError("4-bit bitsandbytes experiment requires NVIDIA CUDA. Use --quantization none or CUDA computer.")
        args.update({
            "device_map": {"": 0},
            "quantization_config": BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=torch.float16,
            ),
        })
    else:
        args.update({"torch_dtype": torch.float16 if torch.cuda.is_available() else torch.float32})
    model = AutoModelForCausalLM.from_pretrained(base_id, **args)
    if quantization == "none" and torch.cuda.is_available():
        model.to("cuda")
    if adapter_path:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, adapter_path)
    model.eval()
    return model, tokenizer, base_id


def predict(model, tokenizer, prompt: str, max_new_tokens: int) -> tuple[str, int]:
    import torch

    messages = [{"role": "user", "content": prompt}]
    inputs = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, tokenize=True, return_dict=True, return_tensors="pt"
    )
    device = next(model.parameters()).device
    inputs = {key: value.to(device) for key, value in inputs.items()}
    with torch.inference_mode():
        output = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.pad_token_id,
        )
    result = output[0][inputs["input_ids"].shape[-1]:]
    return tokenizer.decode(result, skip_special_tokens=True).strip(), len(result)
