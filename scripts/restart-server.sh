#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/stop-server.sh" "${1:-}"
"$SCRIPT_DIR/start-server.sh" "${1:-}"
