#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
pip3 install -q -r requirements.txt
python3 scripts/run_pipeline.py
