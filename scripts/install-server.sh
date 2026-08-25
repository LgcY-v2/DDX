#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILT_BINARY="$ROOT_DIR/build/ddnet-map-voting/DDNet-Server"
. "$ROOT_DIR/scripts/server-targets.sh"

if [[ ! -x "$BUILT_BINARY" ]]; then
	echo "Server build is missing; run scripts/build-server.sh first." >&2
	exit 1
fi

if (($# == 0)); then
	echo "Usage: $0 {ddx-testing|ddx-aip-race} [...]" >&2
	exit 2
fi

for target in "$@"; do
	ddx_select_target "$target"
	RUNTIME_BINARY="$DDX_TARGET_ROOT/build/ddnet/DDNet-Server"
	if [[ ! -x "$RUNTIME_BINARY" ]]; then
		echo "Refusing to create an unprovisioned deployment binary: $RUNTIME_BINARY" >&2
		exit 1
	fi
	TEMP_BINARY="$(mktemp "$(dirname "$RUNTIME_BINARY")/.DDNet-Server.XXXXXX")"
	cleanup() {
		rm -f -- "$TEMP_BINARY"
	}
	trap cleanup EXIT
	install -m 755 "$BUILT_BINARY" "$TEMP_BINARY"
	chown --reference="$RUNTIME_BINARY" "$TEMP_BINARY"
	mv -f -- "$TEMP_BINARY" "$RUNTIME_BINARY"
	TEMP_BINARY=""
	trap - EXIT
	cmp --silent "$BUILT_BINARY" "$RUNTIME_BINARY"
	echo "Installed $target binary at $RUNTIME_BINARY; restart that target to activate it."
done
