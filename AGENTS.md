# AGENTS.md

本文件是 AI 编码工具在本仓库工作时的行为准则。**「合并门禁」章节为强制要求，不得绕过。**

## 项目定位

AI Infra 学习与实验仓库。当前阶段：环境基线与工具链（推理引擎 / KV cache / 调度实验待展开）。
技术栈：Python 3.11、uv、PyTorch 2.14、pytest、ruff。
硬件：RTX 4060 Laptop（8 GB 显存，cc 8.9）。详见 `docs/env.md`。

## 常用命令

| 用途 | 命令 |
|---|---|
| 安装/同步依赖 | `uv sync` |
| 全部单测 | `uv run pytest -q` |
| 单个测试文件 | `uv run pytest tests/test_x.py -q` |
| 静态检查 | `uv run ruff check .` |
| 格式检查 | `uv run ruff format --check .` |
| GPU 基准 | `uv run python bench/run.py --tag <标签>` |
| 基准对比 | `uv run python bench/compare.py bench/results/baseline.json <新结果.json>` |
| 环境自检 | `./scripts/check_env.sh` |

## 代码规范

- 类型标注完整；公共函数写 docstring（Google 风格）。
- 不擅自引入新依赖。需要时先说明理由，再用 `uv add`（它会同时更新 `pyproject.toml` 和 `uv.lock`）。
- 不留 `print` 调试残留，统一用 `logging`。
- 所有随机性必须显式设种子（`torch.manual_seed`），否则 benchmark 与测试不可复现。
- GPU 代码必须能在 `torch.cuda.is_available()` 为 False 时优雅跳过（用 `needs_gpu` 标记）。

## 合并门禁（强制）

AI 生成的任何代码，**以下四条全绿才允许标记为完成 / 提交 PR**：

1. **单测**：`uv run pytest -q` 全绿。新增或修改的函数必须有对应测试，覆盖正常路径 + 至少一个边界或异常路径。
2. **静态检查**：`uv run ruff check .` 与 `uv run ruff format --check .` 无报错。
3. **基准不回退**：与 `bench/results/baseline.json` 对比
   - 吞吐下降 > 3% → 阻止合并
   - p50 延迟上升 > 5% → 阻止合并
   - 显存峰值上升 > 5% → 阻止合并
   测量协议：预热 3 轮、正式 ≥20 轮，取 p50；结果写入 `bench/results/`。
4. **结果可复现**：commit message 或 PR 描述里贴出「改动前 / 改动后」的关键数字，以及 `bench` 输出的 JSON 文件名。

任一条不满足时：**不得宣称任务完成**。应说明失败项、给出定位思路，或明确请求人工决策。

## 禁止事项

- 不得为了让测试通过而修改测试断言（除非用户明确同意）。
- 不得删除、跳过或 xfail 失败的测试来「解决」问题。
- 不得缩小 benchmark 的输入规模以获得更好看的数字。
- 不得提交密钥、内网地址、他人账号信息（`docs/env.md` 里只写硬件与软件版本）。
- 不得 `git push --force` 到 main。

## 提交规范

Conventional Commits：`feat:` / `fix:` / `perf:` / `test:` / `docs:` / `chore:`
一条 commit 只做一件事。性能相关改动必须用 `perf:` 前缀并在正文给出数字。
