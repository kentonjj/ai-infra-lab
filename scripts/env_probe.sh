#!/usr/bin/env bash
# 采集环境信息，输出一段 Markdown，粘贴进 docs/env.md
# 用法：bash scripts/env_probe.sh
set -u

hr() { printf '\n### %s\n\n```text\n' "$1"; }
end() { printf '```\n'; }

echo "# 环境采集 $(date '+%F %T %Z')"

hr "系统"
. /etc/os-release 2>/dev/null && echo "${PRETTY_NAME:-unknown}"
uname -srm
end

hr "CPU / 内存"
LANG=C lscpu 2>/dev/null | grep -E 'Model name|^CPU\(s\):' | sed 's/  */ /g'
free -h 2>/dev/null | sed -n '1,2p'
end

hr "GPU"
if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv 2>&1 || true
  nvidia-smi 2>/dev/null | grep -m1 'CUDA Version' || true
else
  echo "nvidia-smi: 未安装 / 不可用"
fi
lspci 2>/dev/null | grep -i -E 'vga|3d|nvidia' || echo "lspci: 无输出"
if compgen -G "/dev/nvidia*" >/dev/null 2>&1; then
  ls -d /dev/nvidia* 2>/dev/null | head -6
else
  echo "/dev/nvidia*: 不存在（驱动未加载，或当前是容器/沙箱环境）"
fi
end

hr "Python / 工具链"
python3 --version 2>&1
if command -v uv >/dev/null 2>&1; then uv --version; else echo "uv: 未安装"; fi
git --version 2>&1
node --version 2>/dev/null || true
end

hr "磁盘"
df -h . 2>/dev/null | tail -2
end
