#!/usr/bin/env bash
# lili-ai-coach 安装器（bash 便捷封装）
# 真正的安装逻辑在 install.py（跨平台单源）；本脚本只是调用它。
# 用法： bash install.sh [--src DIR] [--target DIR] [--harness workbuddy|hermes|codex] [--dry-run]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${PYTHON:-python3}"

if ! command -v "$PY" >/dev/null 2>&1; then
  echo "[install][ERROR] 未找到 python3，请先安装 Python 3。" >&2
  exit 1
fi

exec "$PY" "$SCRIPT_DIR/install.py" "$@"
