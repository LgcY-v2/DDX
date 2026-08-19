#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SYSROOT="$ROOT_DIR/.toolchain/sysroot"
CARGO_HOME="$ROOT_DIR/.toolchain/cargo"
RUSTUP_HOME="$ROOT_DIR/.toolchain/rustup"
CC="$SYSROOT/usr/bin/x86_64-linux-gnu-gcc-15"
CXX="$SYSROOT/usr/bin/x86_64-linux-gnu-g++-15"
CMAKE="$SYSROOT/usr/bin/cmake"
NINJA="$SYSROOT/usr/bin/ninja"

export PATH="$CARGO_HOME/bin:$SYSROOT/usr/bin:/usr/bin:/bin"
export LD_LIBRARY_PATH="$SYSROOT/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export CARGO_HOME RUSTUP_HOME CC CXX
export CARGO_TARGET_X86_64_UNKNOWN_LINUX_GNU_LINKER="$CC"

for executable in "$CC" "$CXX" "$CMAKE" "$NINJA" "$CARGO_HOME/bin/cargo"; do
	if [[ ! -x "$executable" ]]; then
		echo "The project toolchain is incomplete: $executable is missing." >&2
		exit 1
	fi
done

"$CMAKE" -S "$ROOT_DIR/source/ddnet" -B "$ROOT_DIR/build/ddnet" -G Ninja \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_C_COMPILER="$CC" \
	-DCMAKE_CXX_COMPILER="$CXX" \
	-DCLIENT=OFF \
	-DSERVER=ON \
	-DTOOLS=OFF \
	-DPREFER_BUNDLED_LIBS=ON \
	-DMYSQL=OFF \
	-DWEBSOCKETS=OFF \
	-DUPNP=OFF \
	-DVULKAN=OFF \
	-DVIDEORECORDER=OFF \
	-DAUTOUPDATE=OFF \
	-DDOWNLOAD_GTEST=OFF

"$CMAKE" --build "$ROOT_DIR/build/ddnet" --target DDNet-Server -j "${JOBS:-2}"

echo "Built $ROOT_DIR/build/ddnet/DDNet-Server"
