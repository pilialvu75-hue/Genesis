"""Merge the *verified* CPU pilot LoRA into its base, for GGUF conversion only.

Does not claim the result is the final or a superior Chimera 1 model.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

BASE = "Qwen/Qwen3-0.6B"
EXPECTED_ADAPTER_SHA256 = "510a75e163f4c5e76d2987f596fa5020da23ce81a93e352a3bc1b3aa53b6d64c"

def digest(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for part in iter(lambda: f.read(1024*1024), b""):
            h.update(part)
    return h.hexdigest()

def main():
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel
    adapter = Path("inputs/adapter")
    weights = adapter / "adapter_model.safetensors"
    if not weights.is_file():
        raise FileNotFoundError("Missing expected PEFT LoRA artifact")
    sha = digest(weights)
    if sha != EXPECTED_ADAPTER_SHA256:
        raise ValueError(f"Unexpected adapter hash {sha}, refusing merge")
    cfg = json.loads((adapter/"adapter_config.json").read_text(encoding="utf-8"))
    if cfg.get("base_model_name_or_path") != BASE:
        raise ValueError("Adapter belongs to a different base model, refusing merge")
    base = AutoModelForCausalLM.from_pretrained(
        BASE, torch_dtype=torch.float32, low_cpu_mem_usage=True, trust_remote_code=False
    )
    peft = PeftModel.from_pretrained(base, str(adapter), is_trainable=False)
    merged = peft.merge_and_unload(safe_merge=True)
    output = Path("outputs/merged")
    output.mkdir(parents=True, exist_ok=True)
    merged.save_pretrained(output, safe_serialization=True, max_shard_size="2GB")
    AutoTokenizer.from_pretrained(BASE, trust_remote_code=False).save_pretrained(output)
    meta = {
        "kind": "chimera1-pilot-merged-v1",
        "not_final_chimera1": True,
        "base_model": BASE,
        "base_license": "Apache-2.0",
        "source_workflow_run": 42866886858,
        "source_adapter_sha256": sha,
        "training": "CPU LoRA, 12 steps on 24 original text examples",
        "qualification": "Technical conversion/inference trial only; no evidence of increased general intelligence",
    }
    (output/"pilot_provenance.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2)+"\n", encoding="utf-8"
    )
    print(json.dumps(meta, indent=2), flush=True)

if __name__ == "__main__":
    main()
