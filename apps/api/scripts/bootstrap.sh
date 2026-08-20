#!/usr/bin/env bash
# Creates the local virtualenv and installs the API in editable mode with dev extras.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -x .venv/bin/pip ]; then
  rm -rf .venv
  python3 -m venv .venv
fi
./.venv/bin/python -m pip install --quiet --upgrade pip
./.venv/bin/python -m pip install --quiet -e ".[dev]"
