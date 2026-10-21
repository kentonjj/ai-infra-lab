"""冒烟测试：确认环境与基础算子可用。"""

from __future__ import annotations

import torch

from tests.conftest import needs_gpu


def test_torch_importable() -> None:
    assert torch.__version__


def test_cpu_matmul_shape() -> None:
    a = torch.randn(32, 64)
    b = torch.randn(64, 16)
    assert (a @ b).shape == (32, 16)


@needs_gpu
def test_gpu_bf16_matmul() -> None:
    a = torch.randn(512, 512, device="cuda", dtype=torch.bfloat16)
    out = a @ a
    assert out.shape == (512, 512)
    assert out.dtype == torch.bfloat16
    assert torch.isfinite(out).all()
