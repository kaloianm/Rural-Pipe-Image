#/usr/bin/sh

die() {
    echo "$*" 1>&2
    exit 1
}

[ "$#" -eq 1 ] || die "Usage: $0 <cross-compiler name>"

X_COMPILE_ENV_NAME=$1
X_COMPILE_ENV_ROOT=$HOME/x-tools/$X_COMPILE_ENV_NAME
echo "Executing command for cross-compile environment $X_COMPILE_ENV_NAME ..."
echo "Binary path root $X_COMPILE_ENV_ROOT"
shift

export PATH="$X_COMPILE_ENV_ROOT/bin:$PATH"

X_COMPILE_TOOLS_PREFIX="$X_COMPILE_ENV_ROOT/bin/$X_COMPILE_ENV_NAME-"

export X_COMPILE_SYSROOT_PREFIX="$X_COMPILE_ENV_ROOT/$X_COMPILE_ENV_NAME/sysroot"
export X_COMPILE_BUILD_PREFIX="$(dirname $(realpath $0))/build"
export X_COMPILE_STAGING_PREFIX="$(dirname $(realpath $0))/staging"

export CC="${X_COMPILE_TOOLS_PREFIX}gcc"
export CXX="${X_COMPILE_TOOLS_PREFIX}g++"
export LD="${X_COMPILE_TOOLS_PREFIX}ld"
export AR="${X_COMPILE_TOOLS_PREFIX}ar"
export RANLIB="${X_COMPILE_TOOLS_PREFIX}ranlib"
export READELF="${X_COMPILE_TOOLS_PREFIX}readelf"

export PKG_CONFIG_PATH="$X_COMPILE_SYSROOT_PREFIX/usr/lib/pkgconfig:$X_COMPILE_SYSROOT_PREFIX/usr/local/lib/pkgconfig:$X_COMPILE_SYSROOT_PREFIX/usr/lib/arm-linux-gnueabihf/pkgconfig"
export PKG_CONFIG_SYSROOT_DIR="$X_COMPILE_SYSROOT_PREFIX"

mkdir -p ./staging && mkdir -p ./build && cd ./build && exec $SHELL
