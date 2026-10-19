#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd -- "$PROJECT_ROOT"
image=${1:-yedige-batyrkhan-devops:verification}
docker info >/dev/null
docker compose config --quiet
docker build -t "$image" .
container_id=$(docker run -d -e APP_ENV=verification -e STUDENT_ID=38419 "$image")
cleanup() {
    docker rm -f "$container_id" >/dev/null 2>&1 || true
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
if ! docker exec -i "$container_id" python3 - < scripts/http_smoke.py; then
    docker logs "$container_id"
    exit 1
fi
uid=$(docker exec "$container_id" id -u)
[[ "$uid" != 0 ]] || { printf 'Container must not run as root.\n' >&2; exit 1; }
printf 'Docker verification passed; container user ID: %s\n' "$uid"
