# 环境记录（2026-10-21）

- 机器：Lenovo G5000 IRX9，Ubuntu 22.04.5 LTS
- GPU：NVIDIA RTX 4060 Laptop，8188 MiB（可用约 7.6 GiB），cc 8.9，功耗上限 55 W
- 驱动：580.178.04（支持到 CUDA 13.0），模块 nvidia / uvm / drm / modeset 已加载
- Python：3.11.17（uv 0.13.4 管理），PyTorch 2.14.1+cu130
- 验证：cuda.is_available() = True，bf16 4096 matmul 通过
- 边界：可跑 1.5B-7B 4-bit 量化推理与小 batch 压测；跑不动 14B+、多卡、大规模并发
- 后续：正式 benchmark 租 AutoDL 4090 / A100，本机只做功能验证
- 自检：./scripts/check_env.sh
