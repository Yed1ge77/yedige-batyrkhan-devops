#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
demo_dir="$(mktemp -d "$PROJECT_ROOT/logs/linux-demo.XXXXXX")"
child_pid=''
cleanup() {
    if [[ -n "$child_pid" ]]; then
        kill "$child_pid" 2>/dev/null || true
        wait "$child_pid" 2>/dev/null || true
    fi
    # Only remove the unique directory created by this invocation.
    rm -rf -- "$demo_dir"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

cd -- "$demo_dir"
printf '=== pwd: disposable working directory ===\n'
pwd
printf '\n=== mkdir, touch, ls ===\n'
mkdir documents
touch documents/student.txt
ls -la documents
printf 'Student: Batyrkhan Yedige Yerlanuly\nCourse: DevOps\n' > documents/student.txt
printf '\n=== cp and mv ===\n'
cp documents/student.txt documents/copy.txt
mv documents/copy.txt documents/renamed.txt
printf '\n=== find and grep ===\n'
find . -type f -print
grep -n 'DevOps' documents/student.txt
printf '\n=== chmod and file permissions ===\n'
chmod 640 documents/student.txt
ls -l documents/student.txt
stat -c 'Permissions: %a (%A)' documents/student.txt
printf '\n=== rm: remove our copy ===\n'
rm -- documents/renamed.txt
printf '\n=== Process inspection: our temporary sleep process ===\n'
sleep 30 &
child_pid=$!
ps -p "$child_pid" -o pid,ppid,stat,comm
kill "$child_pid"
wait "$child_pid" 2>/dev/null || true
child_pid=''
printf '\nDemo complete. The temporary directory will be removed.\n'
