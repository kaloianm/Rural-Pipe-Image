> **Warning**
> This is work in progress so most of the steps are manual and/or are incomplete.

# RuralPipe Image Builder
This project contains the necessary scripts and automation to build a bootable RuralPipe image for Raspberry Pi 4

# Building the cross-compiler toolchain
This project uses [crosstool-ng](https://crosstool-ng.github.io/) as the means of building the cross-compiler toolchain. Due to the fact that RasPiOS (Raspberry Pi OS) is still on [libc 2.31](https://sourceware.org/git/glibc.git), the compiler needs to stay on GCC 10 since as of the time of this writing, later GCC versions fail to compile older libc versions.

Follow the instructions [here](ct-ng-cross-compiler-rpi4/README.md).

# Installing/compiling prerequisites
The RuralPipe Image uses newer versions of Python, DBus and ModemManager than what natively comes with RasPiOS. Because of this, these utilities need to be cross-compiled first. These utilities in turn depend on libraries, which are also quite old on RasPiOS, so these need to be compiled from source as well.

In addition, the PyMM module uses functionality (such as the `case` statement) which is only present in Python 3.10 and later. These are not readily available on RasPiOS, so they need to be compiled from source as well.

In order to start the cross-compilation environment locally, use the following script which will start a sub-shell with the appropriate environment variables configured.
```
./x-compile-env.sh armv8-RuralPipe-linux-gnueabihf
```

## OPENSSL 3
Openssl3 is a prerequisite for the Python `_ssl` module.
```
git clone --depth 1 --branch openssl-3.0.7 --single-branch https://github.com/openssl/openssl.git
```

### Local compile
```
mkdir build-dev-machine && cd "$_"

../Configure --prefix=/usr/local/ --openssldir=/usr/local/ -Wl,-rpath=/usr/local/lib -Wl,--enable-new-dtags

make -j11
sudo make install
```

### Cross-compile
```
mkdir build-rpi && cd "$_"

../Configure linux-generic32 \
  --prefix=/usr/local --openssldir=/usr/local \
  -Wl,-rpath=/usr/local/lib \
  -Wl,--enable-new-dtags

make -j11
make install DESTDIR=$X_COMPILE_SYSROOT_PREFIX
make install DESTDIR=$X_COMPILE_STAGING_PREFIX/RPI-OpenSSL
```

## PYTHON 3.11
Some of the RuralPipe's modules use functionality from a later Python so we build version 3.11.
```
git clone --depth 1 --branch v3.11.0 --single-branch https://github.com/python/cpython.git
```

### Local compile
```
mkdir build-dev-machine && cd "$_"

../configure -C \
  --prefix=/usr/local \
  --with-openssl=/usr/local --with-openssl-rpath=auto \
  --enable-optimizations \
  --with-computed-gotos

make -j11
sudo make install
sudo ldconfig
```

### Cross-compile
```
mkdir build-rpi && cd "$_"

echo ac_cv_file__dev_ptmx=yes >> config.site
echo ac_cv_file__dev_ptc=no >> config.site

env \
  CONFIG_SITE=config.site \
  CFLAGS="\
    -I$X_COMPILE_SYSROOT_PREFIX/usr/include/arm-linux-gnueabihf \
    -I$X_COMPILE_SYSROOT_PREFIX/usr/include/tirpc \
    " \
  LDFLAGS="\
    -L$X_COMPILE_SYSROOT_PREFIX/lib/arm-linux-gnueabihf \
    -L$X_COMPILE_SYSROOT_PREFIX/usr/lib/arm-linux-gnueabihf \
    -Wl,-rpath-link=$X_COMPILE_SYSROOT_PREFIX/lib/arm-linux-gnueabihf \
    -Wl,-rpath-link=$X_COMPILE_SYSROOT_PREFIX/usr/lib/arm-linux-gnueabihf \
    " \
../configure -C \
  --prefix=/usr/local \
  --host=armv8-unknown-linux-gnueabihf --build=aarch64-unknown-linux-gnu \
  --enable-shared \
  --with-openssl=$X_COMPILE_SYSROOT_PREFIX/usr/local \
  --with-openssl-rpath=/usr/local/lib \
  --with-system-expat \
  --with-system-ffi \
  --with-build-python=/usr/local/bin/python3.11 \
  --enable-optimizations \
  --with-computed-gotos \
  --disable-ipv6

make -j11

patchelf --add-needed /usr/lib/arm-linux-gnueabihf/libffi.so.7 ./build/lib.linux-arm-3.11/_ctypes.cpython-311-arm-linux-gnueabihf.so
patchelf --add-needed /lib/arm-linux-gnueabihf/libexpat.so.1 ./build/lib.linux-arm-3.11/pyexpat.cpython-311-arm-linux-gnueabihf.so

make install DESTDIR=$X_COMPILE_SYSROOT_PREFIX
make install DESTDIR=$X_COMPILE_STAGING_PREFIX/RPI-Python3
```

## DBUS 1.14
The dbus library is a prerequisite for the ModemManager service.
```
git clone --depth 1 --branch dbus-1.14.4 --single-branch https://gitlab.freedesktop.org/dbus/dbus.git
```

### Local compile
```
TODO
```

### Cross-compile
```
env \
  CFLAGS="\
    -I$X_COMPILE_SYSROOT_PREFIX/usr/include/arm-linux-gnueabihf \
    -I$X_COMPILE_SYSROOT_PREFIX/usr/include/tirpc \
    " \
  LDFLAGS="\
    -L$X_COMPILE_SYSROOT_PREFIX/lib/arm-linux-gnueabihf \
    -L$X_COMPILE_SYSROOT_PREFIX/usr/lib/arm-linux-gnueabihf \
    -Wl,-rpath-link=$X_COMPILE_SYSROOT_PREFIX/lib/arm-linux-gnueabihf \
    -Wl,-rpath-link=$X_COMPILE_SYSROOT_PREFIX/usr/lib/arm-linux-gnueabihf \
    " \
./autogen.sh \
  --prefix=/usr/local \
  --host=armv8-unknown-linux-gnueabihf --build=aarch64-unknown-linux-gnu \
  --enable-shared \
  --disable-Werror \
  --with-system-socket=/run/dbus/system_bus_socket \
  --with-session-socket-dir=/var/run/dbus/system_bus_socket

make -j11
make install DESTDIR=$X_COMPILE_SYSROOT_PREFIX
make install DESTDIR=$X_COMPILE_STAGING_PREFIX/RPI-DBus
```

## GLib 2.58.3
The Glib library is prerequisite for the ModemManager service.
```
git clone --depth 1 --branch 2.58.3 --single-branch https://gitlab.gnome.org/GNOME/glib.git
```

### Local compile
```
TODO
```

### Cross-compile
```
echo glib_cv_stack_grows=no >> config.site
echo glib_cv_uscore=yes >> config.site

env \
  CONFIG_SITE=config.site \
  CFLAGS="\
    -I$X_COMPILE_SYSROOT_PREFIX/usr/include/arm-linux-gnueabihf \
    -I$X_COMPILE_SYSROOT_PREFIX/usr/include/tirpc \
    " \
  LDFLAGS="\
    -L$X_COMPILE_SYSROOT_PREFIX/lib/arm-linux-gnueabihf \
    -L$X_COMPILE_SYSROOT_PREFIX/usr/lib/arm-linux-gnueabihf \
    -Wl,-rpath-link=$X_COMPILE_BUILD_PREFIX/glib/gmodule/.libs \
    -Wl,-rpath-link=$X_COMPILE_SYSROOT_PREFIX/lib/arm-linux-gnueabihf \
    -Wl,-rpath-link=$X_COMPILE_SYSROOT_PREFIX/usr/lib/arm-linux-gnueabihf \
    " \
./autogen.sh \
  --prefix=/usr/local \
  --host=armv8-unknown-linux-gnueabihf --build=aarch64-unknown-linux-gnu \
  --enable-shared \
  --with-pcre=internal \
  --with-python=python3

make -j11
make install DESTDIR=$X_COMPILE_SYSROOT_PREFIX
make install DESTDIR=$X_COMPILE_STAGING_PREFIX/RPI-Glib
```

## LibMBIM 1.26.4
```
git clone --depth 1 --branch 1.26.4 --single-branch https://gitlab.freedesktop.org/mobile-broadband/libmbim.git
```

### Local compile
```
TODO
```

### Cross-compile
```
env \
  CFLAGS="\
    -I$X_COMPILE_SYSROOT_PREFIX/usr/include/arm-linux-gnueabihf \
    -I$X_COMPILE_SYSROOT_PREFIX/usr/include/tirpc \
    " \
  LDFLAGS="\
    -L$X_COMPILE_SYSROOT_PREFIX/lib/arm-linux-gnueabihf \
    -L$X_COMPILE_SYSROOT_PREFIX/usr/lib/arm-linux-gnueabihf \
    -Wl,-rpath-link=$X_COMPILE_SYSROOT_PREFIX/lib/arm-linux-gnueabihf \
    -Wl,-rpath-link=$X_COMPILE_SYSROOT_PREFIX/usr/lib/arm-linux-gnueabihf \
    " \
./autogen.sh \
  --prefix=/usr/local \
  --host=armv8-unknown-linux-gnueabihf --build=aarch64-unknown-linux-gnu \
  --enable-shared \
  --disable-Werror

make -j11
make install DESTDIR=$X_COMPILE_SYSROOT_PREFIX
make install DESTDIR=$X_COMPILE_STAGING_PREFIX/RPI-LibMBIM
```

## LibQRTR 1.0.0
```
git clone --depth 1 --branch 1.0.0 --single-branch https://gitlab.freedesktop.org/mobile-broadband/libqrtr-glib.git
```

### Local compile
```
TODO
```

### Cross-compile
```
env \
  CFLAGS="\
    -I$X_COMPILE_SYSROOT_PREFIX/usr/include/arm-linux-gnueabihf \
    -I$X_COMPILE_SYSROOT_PREFIX/usr/include/tirpc \
    " \
  LDFLAGS="\
    -L$X_COMPILE_SYSROOT_PREFIX/lib/arm-linux-gnueabihf \
    -L$X_COMPILE_SYSROOT_PREFIX/usr/lib/arm-linux-gnueabihf \
    -Wl,-rpath-link=$X_COMPILE_SYSROOT_PREFIX/lib/arm-linux-gnueabihf \
    -Wl,-rpath-link=$X_COMPILE_SYSROOT_PREFIX/usr/lib/arm-linux-gnueabihf \
    " \
./autogen.sh \
  --prefix=/usr/local \
  --host=armv8-unknown-linux-gnueabihf --build=aarch64-unknown-linux-gnu \
  --enable-shared \
  --disable-Werror

make -j11
make install DESTDIR=$X_COMPILE_SYSROOT_PREFIX
make install DESTDIR=$X_COMPILE_STAGING_PREFIX/RPI-LibQRTR
```

## LibQMI 1.30.8
```
git clone --depth 1 --branch 1.30.8 --single-branch https://gitlab.freedesktop.org/mobile-broadband/libqmi.git
```

### Local compile
```
TODO
```

### Cross-compile
```
env \
  CFLAGS="\
    -I$X_COMPILE_SYSROOT_PREFIX/usr/include/arm-linux-gnueabihf \
    -I$X_COMPILE_SYSROOT_PREFIX/usr/include/tirpc \
    " \
  LDFLAGS="\
    -L$X_COMPILE_SYSROOT_PREFIX/lib/arm-linux-gnueabihf \
    -L$X_COMPILE_SYSROOT_PREFIX/usr/lib/arm-linux-gnueabihf \
    -Wl,-rpath-link=$X_COMPILE_SYSROOT_PREFIX/lib/arm-linux-gnueabihf \
    -Wl,-rpath-link=$X_COMPILE_SYSROOT_PREFIX/usr/lib/arm-linux-gnueabihf \
    " \
./autogen.sh \
  --prefix=/usr/local \
  --host=armv8-unknown-linux-gnueabihf --build=aarch64-unknown-linux-gnu \
  --enable-shared \
  --disable-Werror

make -j11
make install DESTDIR=$X_COMPILE_SYSROOT_PREFIX
make install DESTDIR=$X_COMPILE_STAGING_PREFIX/RPI-LibQMI
```

## ModemManager 1.18
```
git clone --depth 1 --branch 1.18.12 --single-branch https://gitlab.freedesktop.org/mobile-broadband/ModemManager.git
```

### Local compile
```
TODO
```

### Cross-compile
```
git apply ../../patches/ModemManager-1.18.12-glib-bin-pkg-config.patch

env \
  CFLAGS="\
    -I$X_COMPILE_SYSROOT_PREFIX/usr/include/arm-linux-gnueabihf \
    -I$X_COMPILE_SYSROOT_PREFIX/usr/include/tirpc \
    " \
  LDFLAGS="\
    -L$X_COMPILE_SYSROOT_PREFIX/lib/arm-linux-gnueabihf \
    -L$X_COMPILE_SYSROOT_PREFIX/usr/lib/arm-linux-gnueabihf \
    -Wl,-rpath-link=$X_COMPILE_SYSROOT_PREFIX/lib/arm-linux-gnueabihf \
    -Wl,-rpath-link=$X_COMPILE_SYSROOT_PREFIX/usr/lib/arm-linux-gnueabihf \
    " \
./autogen.sh \
  --prefix=/usr/local \
  --host=armv8-unknown-linux-gnueabihf --build=aarch64-unknown-linux-gnu \
  --enable-shared \
  --disable-Werror

make -j11
make install DESTDIR=$X_COMPILE_STAGING_PREFIX/RPI-ModemManager
```

## GLIBC (Optional)
```
git clone --depth 1 --branch release/2.36/master --single-branch https://sourceware.org/git/glibc.git
```

### Local compile
```
TODO
```

### Cross-compile
```
mkdir build-rpi && cd "$_"

env \
  CHOST=armhf \
../configure \
  --prefix=/usr/local \
  --host=armv8-unknown-linux-gnueabihf --build=aarch64-unknown-linux-gnu \
  --disable-sanity-checks

make -j11
make install DESTDIR=$X_COMPILE_STAGING_PREFIX/RPI-GlibC
```
