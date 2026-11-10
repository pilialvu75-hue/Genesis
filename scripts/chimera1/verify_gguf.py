"""Validate GGUF payload and write a machine-readable hash/size manifest."""
from __future__ import annotations

import hashlib
import json
import pathlib

def sha256_file(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    path=pathlib.Path("outputs/chimera1-pilot-qwen3-0.6b-q4_k_m.gguf")
    if not path.is_file() or path.stat().st_size < 50_000_000:
        raise RuntimeError("Quantised GGUF is absent or implausibly small")
    with path.open("rb") as file:
        magic=file.read(4)
    if magic != b"GGUF":
        raise RuntimeError(f"Not a GGUF file: {magic!r}")
    smoke=pathlib.Path("outputs/llama_inference.txt")
    if not smoke.is_file() or not smoke.read_text(errors="replace").strip():
        raise RuntimeError("No llama.cpp inference output found")
    manifest={
        "schema":"chimera.gguf.cpu-pilot.v1",
        "file":path.name,
        "size_bytes":path.stat().st_size,
        "sha256":sha256_file(path),
        "format":"GGUF quantised Q4_K_M",
        "base":"Qwen/Qwen3-0.6B",
        "pilot_adapter_sha256":"510a75e163f4c5e76d2987f596fa5020da23ce81a93e352a3bc1b3aa53b6d64c",
        "source_git_actions_run":42866886858,
        "status":"PILOT_GGUF_TECHNICAL_TEST_ONLY",
        "warnings":["NOT Chimera 1 ready", "NOT validated on ASUS/AIVEXUS", "NOT proof of improved capabilities"],
    }
    pathlib.Path("outputs/gguf-manifest.json").write_text(
        json.dumps(manifest,ensure_ascii=False,indent=2)+"\n", encoding="utf-8"
    )
    print(json.dumps(manifest,ensure_ascii=False,indent=2))
if __name__=="__main__":
    main()
