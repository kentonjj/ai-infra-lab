#!/usr/bin/env bash
set -uo pipefail

echo "===== OS ====="
(lsb_release -ds 2>/dev/null || head -2 /etc/os-release)

echo "===== 工具链 ====="
git --version
uv --version
python -V 2>/dev/null || echo "python: 未在虚拟环境中"

echo "===== GPU ====="
if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi --query-gpu=index,name,memory.total,driver_version,compute_cap --format=csv
  nvidia-smi --query-gpu=temperature.gpu,power.draw,power.limit,clocks.sm --format=csv,noheader
else
  echo "nvidia-smi: 未安装（无 NVIDIA 驱动或无独显）"
fi

echo "===== PyTorch ====="
uv run python - <<'PY' 2>/dev/null || echo "torch: 未安装"
import torch
print("torch      :", torch.__version__, "| cuda build:", torch.version.cuda)
print("cuda avail :", torch.cuda.is_available())
if torch.cuda.is_available():
    p = torch.cuda.get_device_properties(0)
    print(f"device     : {p.name} | {p.total_memory/2**30:.1f} GiB | cc {p.major}.{p.minor}")
PY
