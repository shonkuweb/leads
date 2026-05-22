#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONPATH="${PYTHONPATH:-}:$(pwd)/scripts"
python3 scripts/run_discovery_cycle.py
python3 scripts/build_india_school_leads.py
