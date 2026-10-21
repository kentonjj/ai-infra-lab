"""pytest 公共夹具。"""

from __future__ import annotations

import pytest
import torch


@pytest.fixture(autouse=True)
def seed() -> None:
    """所有测试固定随机种子，保证可复现。"""
    torch.manual_seed(0)


needs_gpu = pytest.mark.skipif(
    not torch.cuda.is_available(), reason="需要可用的 CUDA 设备"
)
