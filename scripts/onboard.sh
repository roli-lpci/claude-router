#!/usr/bin/env bash
# onboard.sh — fresh-machine install for claude-router. Idempotent. Exit 0 on success.
set -euo pipefail

DRY_RUN=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    -h|--help) echo "Usage: $0 [--dry-run]"; exit 0 ;;
  esac
done

run() {
  echo "+ $*"
  [ "$DRY_RUN" = "0" ] && "$@"
}

if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)'; then
  echo "ERROR: need Python >= 3.10" >&2
  exit 1
fi

[ -d ".venv" ] || run python3 -m venv .venv
[ "$DRY_RUN" = "0" ] && source .venv/bin/activate
run pip install --upgrade pip --quiet
run pip install --quiet -e ".[dev]" || run pip install --quiet -e .

if [ "$DRY_RUN" = "0" ]; then
  python3 -c "import claude_router; print('claude-router', claude_router.__version__)" >/dev/null
  echo "onboard: OK (note: routing requires 'ollama serve' + 'ollama pull nomic-embed-text')"
fi
