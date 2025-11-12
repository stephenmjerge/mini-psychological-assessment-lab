#!/usr/bin/env bash
set -euo pipefail

# If pytest can't create its cache directory (e.g., sandboxed FS), disable the cache plugin.
if ! mkdir -p .pytest_cache 2>/dev/null; then
  export PYTEST_ADDOPTS="${PYTEST_ADDOPTS:-} -p no:cacheprovider"
fi

exec pytest "$@"
