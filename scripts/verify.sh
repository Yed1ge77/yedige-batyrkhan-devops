#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd -- "$PROJECT_ROOT"
python3 -m unittest discover -s tests -v
python3 -m compileall -q app tests
for script in scripts/*.sh; do bash -n "$script"; done
if command -v shellcheck >/dev/null 2>&1; then
    shellcheck scripts/*.sh
else
    printf 'ShellCheck not installed; optional check skipped.\n'
fi
