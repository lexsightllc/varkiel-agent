#!/usr/bin/env bash
# SPDX-License-Identifier: MPL-2.0
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)

export PYTHONPATH="$REPO_ROOT/src:${PYTHONPATH:-}"
export PIP_DISABLE_PIP_VERSION_CHECK=1
export PYTHONUNBUFFERED=1

run() {
  echo "[scripts] $*"
  "$@"
}

ensure_venv() {
  if [[ -n "${VIRTUAL_ENV:-}" ]]; then
    return
  fi
  if [[ -d "$REPO_ROOT/.venv" ]]; then
    # shellcheck disable=SC1091
    source "$REPO_ROOT/.venv/bin/activate"
  fi
}

