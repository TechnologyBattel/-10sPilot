#!/usr/bin/env bash
# "Build" for a Python service: install deps and verify the app imports.
set -euo pipefail
cd "$(dirname "$0")/.."
./scripts/bootstrap.sh
./.venv/bin/python -c "from app.main import app; print('api build ok')"
