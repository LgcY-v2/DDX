#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPSTREAM_SOURCE="$ROOT_DIR/source/ddnet"
PATCH_FILES=(
	"$ROOT_DIR/patches/0001-feat-add-map-archive-votes.patch"
	"$ROOT_DIR/patches/0002-feat-brand-server-as-ddx.patch"
	"$ROOT_DIR/patches/0003-feat-add-random-archive-collection-maps.patch"
	"$ROOT_DIR/patches/0004-feat-add-owner-rcon.patch"
	"$ROOT_DIR/patches/0005-feat-target-super-commands.patch"
	"$ROOT_DIR/patches/0006-feat-add-aip.patch"
	"$ROOT_DIR/patches/0007-fix-throttle-archive-map-loads.patch"
	"$ROOT_DIR/patches/0008-chore-tidy-server-sources.patch"
	"$ROOT_DIR/patches/0009-feat-add-grenade-bounces.patch"
	"$ROOT_DIR/patches/0010-feat-add-player-handoffs.patch"
)
PATCHED_SOURCE="$ROOT_DIR/build/source-map-voting"
PATCHED_BUILD="$ROOT_DIR/build/ddnet-map-voting"
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

for executable in "$CC" "$CXX" "$CMAKE" "$NINJA" "$CARGO_HOME/bin/cargo" /usr/bin/git /usr/bin/patch /usr/bin/tar; do
	if [[ ! -x "$executable" ]]; then
		echo "The project toolchain is incomplete: $executable is missing." >&2
		exit 1
	fi
done

EXPECTED_UPSTREAM_REVISION="e5ebaeaad935abc65cf0470a1701877fa258856b"
ACTUAL_UPSTREAM_REVISION="$(/usr/bin/git -C "$UPSTREAM_SOURCE" rev-parse HEAD)"
if [[ "$ACTUAL_UPSTREAM_REVISION" != "$EXPECTED_UPSTREAM_REVISION" ]]; then
	echo "Refusing to patch unexpected DDNet revision $ACTUAL_UPSTREAM_REVISION." >&2
	exit 1
fi
export DDNET_GIT_SHORTREV_HASH="${EXPECTED_UPSTREAM_REVISION:0:16}"
for patch_file in "${PATCH_FILES[@]}"; do
	if [[ ! -f "$patch_file" ]]; then
		echo "Server patch is missing: $patch_file" >&2
		exit 1
	fi
done

install -d -m 755 "$ROOT_DIR/build"
STAGED_SOURCE="$(mktemp -d "$ROOT_DIR/build/.source-map-voting.XXXXXX")"
cleanup() {
	if [[ -n "$STAGED_SOURCE" ]]; then
		rm -rf -- "$STAGED_SOURCE"
	fi
}
trap cleanup EXIT

/usr/bin/git -C "$UPSTREAM_SOURCE" archive --format=tar HEAD | /usr/bin/tar -xf - -C "$STAGED_SOURCE"
rmdir "$STAGED_SOURCE/ddnet-libs"
ln -s "$UPSTREAM_SOURCE/ddnet-libs" "$STAGED_SOURCE/ddnet-libs"
(
	cd "$STAGED_SOURCE"
	for patch_file in "${PATCH_FILES[@]}"; do
		/usr/bin/patch --batch --forward -p1 <"$patch_file"
	done
)

rm -rf -- "$PATCHED_SOURCE"
mv "$STAGED_SOURCE" "$PATCHED_SOURCE"
STAGED_SOURCE=""

"$CMAKE" -S "$PATCHED_SOURCE" -B "$PATCHED_BUILD" -G Ninja \
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

# The environment-provided upstream revision is part of the generated source,
# but CMake cannot track environment changes as dependencies. Refresh the
# generator input so reused build trees cannot retain a stale revision string.
touch "$PATCHED_SOURCE/scripts/git_revision.py"
"$CMAKE" --build "$PATCHED_BUILD" --target DDNet-Server -j "${JOBS:-2}"

echo "Built patched DDNet server at $PATCHED_BUILD/DDNet-Server"
