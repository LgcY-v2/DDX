#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILT_BINARY="$ROOT_DIR/build/ddnet-map-voting/DDNet-Server"
RUNTIME_BINARY="$ROOT_DIR/build/ddnet/DDNet-Server"

if [[ ! -x "$BUILT_BINARY" ]]; then
	echo "Server build is missing; run scripts/build-server.sh first." >&2
	exit 1
fi

install -d -m 755 "$(dirname "$RUNTIME_BINARY")"
install -m 755 "$BUILT_BINARY" "$RUNTIME_BINARY.next"
mv -f "$RUNTIME_BINARY.next" "$RUNTIME_BINARY"

echo "Installed server binary at $RUNTIME_BINARY"
