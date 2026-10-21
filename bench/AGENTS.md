# bench/ 局部规则

- **不得修改 `results/baseline.json`**，除非用户明确要求重设基线。
- 不得为了更好看的数字而缩小 `--size`、减少 `--iters` 或跳过 `torch.cuda.synchronize()`。
- 新增基准必须同时给出：p50 延迟、吞吐、显存峰值，并写入 `results/`。
- 结果必须在 commit message 里引用具体 JSON 文件名。
