#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
. "$ROOT_DIR/scripts/server-targets.sh"
ddx_select_target "${1:-}"
UNIT="$DDX_TARGET_UNIT"

if ! systemctl --user is-active --quiet "$UNIT"; then
	STATE="$(systemctl --user is-active "$UNIT" 2>/dev/null || true)"
	echo "DDNet server is already offline (${STATE:-service not loaded})."
	exit 0
fi

systemctl --user stop "$UNIT"

if systemctl --user is-active --quiet "$UNIT"; then
	echo "DDNet server did not stop cleanly." >&2
	exit 1
fi

echo "DDNet server stopped."
