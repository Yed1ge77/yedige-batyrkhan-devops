#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
failed=0
printf '=== Student information ===\n'
if ! python3 - "$PROJECT_ROOT/config/student_info.json" <<'PY'
import json
import sys
try:
    with open(sys.argv[1], encoding="utf-8") as source:
        student = json.load(source)
    for key in ("full_name", "student_id", "group", "university", "course"):
        value = student[key]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Invalid field: {key}")
        print(f"{key.replace('_', ' ').title()}: {value}")
except (OSError, ValueError, KeyError, TypeError) as error:
    print(f"Cannot read student configuration: {error}", file=sys.stderr)
    sys.exit(1)
PY
then
    failed=1
fi
printf '\n=== System information ===\n'
printf 'Username: %s\n' "$(id -un)"
printf 'Hostname: %s\n' "$(hostname)"
printf 'Kernel: %s\n' "$(uname -r)"
if [[ -r /etc/os-release ]]; then
    grep -E '^(NAME|VERSION|PRETTY_NAME)=' /etc/os-release
else
    printf 'OS information unavailable\n'
fi
printf 'Date: %s\n' "$(date --iso-8601=seconds)"
printf 'Working directory: %s\n' "$PWD"
printf 'Project root: %s\n' "$PROJECT_ROOT"
printf '\n=== Required directories ===\n'
for directory in app scripts config logs backup tests; do
    if [[ -d "$PROJECT_ROOT/$directory" ]]; then
        printf 'OK: %s/\n' "$directory"
    else
        printf 'MISSING directory: %s\n' "$directory" >&2
        failed=1
    fi
done
printf '\n=== Required files ===\n'
for file in app/__init__.py app/main.py app/student.py scripts/system_info.sh scripts/linux_demo.sh config/student_info.json logs/.gitkeep backup/.gitkeep tests/__init__.py tests/test_app.py .gitignore README.md; do
    if [[ -f "$PROJECT_ROOT/$file" ]]; then
        printf 'OK: %s\n' "$file"
    else
        printf 'MISSING file: %s\n' "$file" >&2
        failed=1
    fi
done
printf '\n=== Running processes (first 12 rows) ===\n'
ps -eo pid,ppid,user,stat,comm | sed -n '1,12p'
if (( failed )); then
    printf '\nRequired project checks failed.\n' >&2
    exit 1
fi
printf '\nAll required project checks passed.\n'
