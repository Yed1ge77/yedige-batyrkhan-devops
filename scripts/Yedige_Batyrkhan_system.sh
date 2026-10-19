#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
bash "$PROJECT_ROOT/scripts/system_info.sh"
printf '\n=== Disk usage ===\n'
df -h "$PROJECT_ROOT"
printf '\n=== Memory usage ===\n'
free -h
printf '\n=== Instructor required files ===\n'
for file in Yedige_Batyrkhan_info.txt config/app.conf logs/application.log private.txt public.txt; do
    if [[ ! -f "$PROJECT_ROOT/$file" ]]; then
        printf 'MISSING: %s\n' "$file" >&2
        exit 1
    fi
    printf 'OK: %s\n' "$file"
done
