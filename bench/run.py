"""最小 GPU 基准：bf16 matmul 的延迟 / 吞吐 / 显存峰值。"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import subprocess
import time

import torch


def git_sha() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return out.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return "unknown"


def pctl(vals: list[float], q: float) -> float:
    s = sorted(vals)
    return s[min(len(s) - 1, round(q * (len(s) - 1)))]


def run(size: int, iters: int, warmup: int) -> dict:
    dtype = torch.bfloat16
    a = torch.randn(size, size, device="cuda", dtype=dtype)
    b = torch.randn(size, size, device="cuda", dtype=dtype)
    for _ in range(warmup):
        _ = a @ b
    torch.cuda.synchronize()
    torch.cuda.reset_peak_memory_stats()

    lat: list[float] = []
    for _ in range(iters):
        t0 = time.perf_counter()
        _ = a @ b
        torch.cuda.synchronize()
        lat.append((time.perf_counter() - t0) * 1e3)

    props = torch.cuda.get_device_properties(0)
    p50 = pctl(lat, 0.50)
    return {
        "op": f"matmul_bf16_{size}",
        "iterations": iters,
        "latency_ms": {"p50": p50, "p95": pctl(lat, 0.95), "max": max(lat)},
        "throughput_gflops": 2 * size**3 / (p50 / 1e3) / 1e9,
        "peak_mem_gib": torch.cuda.max_memory_allocated() / 2**30,
        "device": {
            "name": props.name,
            "total_mem_gib": round(props.total_memory / 2**30, 2),
            "cc": f"{props.major}.{props.minor}",
        },
        "torch": torch.__version__,
        "git_sha": git_sha(),
        "timestamp": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", type=int, default=4096)
    ap.add_argument("--iters", type=int, default=20)
    ap.add_argument("--warmup", type=int, default=3)
    ap.add_argument("--tag", default="run")
    ap.add_argument("--out-dir", default="bench/results")
    args = ap.parse_args()

    if not torch.cuda.is_available():
        raise SystemExit("CUDA 不可用，无法运行 benchmark")

    res = run(args.size, args.iters, args.warmup)
    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{dt.datetime.now():%Y-%m-%d-%H%M%S}-{args.tag}.json"
    path.write_text(json.dumps(res, indent=2, ensure_ascii=False))

    print(
        f"device      : {res['device']['name']} ({res['device']['total_mem_gib']} GiB)"
    )
    print(f"p50 latency : {res['latency_ms']['p50']:.2f} ms")
    print(f"throughput  : {res['throughput_gflops']:.1f} GFLOP/s")
    print(f"peak mem    : {res['peak_mem_gib']:.2f} GiB")
    print(f"written to  : {path}")


if __name__ == "__main__":
    main()
