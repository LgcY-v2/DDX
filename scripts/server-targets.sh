#!/usr/bin/env bash

ddx_select_target() {
	case "${1:-}" in
	ddx-testing)
		DDX_TARGET_ROOT=/srv/ddx_testing
		DDX_TARGET_UNIT=tee-world-candidate-testing-ddnet.service
		DDX_TARGET_PORT=8305
		;;
	ddx-aip-race)
		DDX_TARGET_ROOT=/srv/ddx_aip_race
		DDX_TARGET_UNIT=ddx-aip-race-ddnet.service
		DDX_TARGET_PORT=8306
		;;
	*)
		echo "Usage: $0 {ddx-testing|ddx-aip-race}" >&2
		return 2
		;;
	esac
}
