#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p -- "$PROJECT_ROOT/logs"
# Append a clearly labelled sample. Preserve any existing log contents.
for number in {1..12}; do
    severity=INFO
    case "$number" in
        4|9) severity=WARNING ;;
        6|11) severity=ERROR ;;
    esac
    printf '%s %s SAMPLE simulated lab event %02d\n' "$(date --iso-8601=seconds)" "$severity" "$number"
done >> "$PROJECT_ROOT/logs/application.log"
printf 'Appended 12 simulated entries to logs/application.log\n'
