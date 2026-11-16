#!/usr/bin/env bash
set -euo pipefail

mkdir -p reports test-results
python -m pytest "$@"
