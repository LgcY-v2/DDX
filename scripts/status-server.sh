#!/usr/bin/env bash
set -euo pipefail

UNIT="tee-world-candidate-testing-ddnet.service"
PORT=8305

if ! systemctl --user is-active --quiet "$UNIT"; then
	STATE="$(systemctl --user is-active "$UNIT" 2>/dev/null || true)"
	echo "offline: ${STATE:-service not loaded}"
	exit 1
fi

PID="$(systemctl --user show "$UNIT" --property=MainPID --value)"
SOCKET="$(ss -H -lunp "sport = :$PORT" 2>/dev/null || true)"
if [[ -z "$SOCKET" || "$SOCKET" != *"pid=$PID,"* ]]; then
	echo "degraded: service PID $PID does not own UDP $PORT"
	exit 1
fi

echo "online: PID $PID, UDP $PORT"
echo "$SOCKET"
