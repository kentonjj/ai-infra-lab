#!/usr/bin/env bash
# 初始化本仓库的工具链：uv + Python 3.11 + .venv（全部装在本仓库内，不污染系统）
# 用法：bash scripts/bootstrap_env.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLS="$ROOT/.tools"
export UV_INSTALL_DIR="$TOOLS"
export UV_PYTHON_INSTALL_DIR="$TOOLS/python"
export UV_CACHE_DIR="$ROOT/.cache/uv"
mkdir -p "$TOOLS" "$UV_CACHE_DIR"

if [ -x "$TOOLS/uv" ]; then
  UV="$TOOLS/uv"
elif command -v uv >/dev/null 2>&1; then
  UV="$(command -v uv)"
else
  echo "==> 安装 uv 到 $TOOLS"
  curl -LsSf https://astral.sh/uv/install.sh | sh
  UV="$TOOLS/uv"
fi

"$UV" --version

echo "==> 安装 Python 3.11（仅本仓库）"
"$UV" python install 3.11

echo "==> 创建虚拟环境 .venv"
if [ -d "$ROOT/.venv" ]; then
  echo "    .venv 已存在，跳过（如需重建请先手动删除）"
else
  "$UV" venv --python 3.11 "$ROOT/.venv"
fi
"$ROOT/.venv/bin/python" -V

cat <<'TIP'

完成。接下来：
  source .venv/bin/activate
  uv pip install vllm        # 10/24 再做
如果 GitHub 下载超时，用国内镜像或先在能访问外网的机器上执行本脚本。
TIP

TIP
