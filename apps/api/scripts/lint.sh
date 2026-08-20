#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
./scripts/bootstrap.sh
./.venv/bin/ruff check app tests
./.venv/bin/ruff format --check app tests
