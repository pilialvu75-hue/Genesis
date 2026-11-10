"""Local diagnostic with optional PyTorch probing; no downloads."""

from __future__ import annotations

import importlib.util
import os
import platform
import shutil
from pathlib import Path


def doctor() -> dict:
    disk = shutil.disk_usage(Path.home())
    report = {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "cpu_count": os.cpu_count(),
        "disk_free_gb": round(disk.free / 1024**3, 2),
        "torch_installed": importlib.util.find_spec("torch") is not None,
    }
    if report["torch_installed"]:
        import torch
        report["torch_version"] = torch.__version__
        report["cuda_available"] = torch.cuda.is_available()
        if torch.cuda.is_available():
            report["gpus"] = [
                {
                    "name": torch.cuda.get_device_name(i),
                    "vram_gb": round(torch.cuda.get_device_properties(i).total_memory / 1024**3, 2),
                }
                for i in range(torch.cuda.device_count())
            ]
    return report
