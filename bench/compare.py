"""对比两个 benchmark 结果；出现回退时以非 0 退出码阻止合并。"""

from __future__ import annotations

import argparse
import json
import sys

MAX_LATENCY_REGRESSION = 0.05
MAX_MEM_REGRESSION = 0.05
MAX_THROUGHPUT_DROP = 0.03


def load(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def rel(new: float, old: float) -> float:
    return (new - old) / old if old else 0.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("baseline")
    ap.add_argument("candidate")
    args = ap.parse_args()

    base, cand = load(args.baseline), load(args.candidate)

    checks = [
        (
            "p50 latency ms",
            base["latency_ms"]["p50"],
            cand["latency_ms"]["p50"],
            rel(cand["latency_ms"]["p50"], base["latency_ms"]["p50"]),
            MAX_LATENCY_REGRESSION,
        ),
        (
            "throughput GFLOP/s",
            base["throughput_gflops"],
            cand["throughput_gflops"],
            -rel(cand["throughput_gflops"], base["throughput_gflops"]),
            MAX_THROUGHPUT_DROP,
        ),
        (
            "peak mem GiB",
            base["peak_mem_gib"],
            cand["peak_mem_gib"],
            rel(cand["peak_mem_gib"], base["peak_mem_gib"]),
            MAX_MEM_REGRESSION,
        ),
    ]

    failed = False
    for name, old, new, delta, limit in checks:
        ok = delta <= limit
        failed |= not ok
        print(
            f"[{'OK  ' if ok else 'FAIL'}] {name}: {old:.4g} -> {new:.4g} "
            f"({delta * 100:+.2f}%, 上限 {limit * 100:.0f}%)"
        )

    if failed:
        print("\n检测到回退，阻止合并。")
        return 1
    print("\n通过，未检测到可测回退。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
