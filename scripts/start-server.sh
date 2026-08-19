#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVER_DIR="$ROOT_DIR/server"
BINARY="$ROOT_DIR/build/ddnet/DDNet-Server"
CONSOLE_LOG="$SERVER_DIR/logs/console.log"
UNIT="tee-world-candidate-testing-ddnet.service"
PORT=8305

install -d -m 700 "$SERVER_DIR/logs" "$SERVER_DIR/run" "$SERVER_DIR/state"

if [[ ! -x "$BINARY" ]]; then
	echo "DDNet server binary is missing; run scripts/build-server.sh first." >&2
	exit 1
fi

socket_for_pid() {
	local pid="$1"
	local socket
	socket="$(ss -H -lunp "sport = :$PORT" 2>/dev/null || true)"
	[[ -n "$socket" && "$socket" == *"pid=$pid,"* ]]
}

if systemctl --user is-active --quiet "$UNIT"; then
	PID="$(systemctl --user show "$UNIT" --property=MainPID --value)"
	if socket_for_pid "$PID"; then
		echo "DDNet server is already online (PID $PID, UDP $PORT)."
		exit 0
	fi
	echo "Service $UNIT is active, but PID $PID does not own UDP $PORT." >&2
	exit 1
fi

systemctl --user reset-failed "$UNIT" 2>/dev/null || true
systemctl --user start "$UNIT"

for _ in {1..50}; do
	if systemctl --user is-active --quiet "$UNIT"; then
		PID="$(systemctl --user show "$UNIT" --property=MainPID --value)"
		if socket_for_pid "$PID"; then
			echo "DDNet server started (PID $PID, UDP $PORT)."
			exit 0
		fi
	fi
	sleep 0.1
done

echo "DDNet server failed to become ready. Recent service and console output:" >&2
systemctl --user --no-pager --full status "$UNIT" >&2 || true
tail -n 80 "$CONSOLE_LOG" >&2 || true
exit 1
