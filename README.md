> **Warning**
> This is work in progress so most of the steps are manual and/or are incomplete.

# RuralPipe Image Builder
This project contains the necessary scripts and automation to build a bootable RuralPipe image for Raspberry Pi 4

# Building the cross-compiler toolchain
This project uses [crosstool-ng](https://crosstool-ng.github.io/) as the means of building the cross-compiler toolchain. Due to the fact that RaspiOS is still on [libc 2.31](https://sourceware.org/git/glibc.git), the compiler needs to stay on GCC 10 since as of the time of this writing, later GCC versions fail to compile older libc versions.

# Manual compilation steps
## OPENSSL 3
Openssl-3 is a prerequisite for the Python SSL module.

### Local compile
```
./Configure --prefix=/opt/openssl3 --openssldir=/opt/openssl3 -Wl,-rpath=/opt/openssl3/lib -Wl,--enable-new-dtags

make -j9
make install
```

### Cross-compile
```
x-compile.sh armv8-rpi4-linux-gnueabihf \
  './Configure linux-generic32 \
   --prefix=/usr/local --openssldir=/usr/local -Wl,-rpath=/usr/local/lib -Wl,--enable-new-dtags'

make -j9
make install DESTDIR=$HOME/workspace/rpi/install
```

## ZLIB
zLib is a prerequisite for the Python zlib module.

### Local compile
```
TODO
```

### Cross-compile
```
x-compile.sh armv8-rpi4-linux-gnueabihf 'CHOST=arm ./configure --prefix=/usr/local'

make -j9
make install DESTDIR=$HOME/workspace/rpi/install
```

## LIBFFI
Libffi is a prerequisite for Python's `_ctypes` module.

### Local compile
```
TODO
```

### Cross-compile
```
autogen.sh
x-compile.sh armv8-rpi4-linux-gnueabihf './configure --prefix=/usr/local --host=armv7l-unknown-linux-gnueabihf'

make -j9
make install DESTDIR=$HOME/workspace/rpi/install
```

## PYTHON 3.11
### Local compile
```
./configure --prefix=/opt/python/3.11.0/ --with-openssl=/opt/openssl3 --with-openssl-rpath=auto --enable-optimizations --with-lto --with-computed-gotos --with-system-ffi
```

### Cross-compile
```
echo ac_cv_file__dev_ptc=no >> config.site
echo ac_cv_file__dev_ptmx=no >> config.site

x-compile.sh armv8-rpi4-linux-gnueabihf \
  'CONFIG_SITE=config.site \
   CC="$CC -I$HOME/workspace/rpi/install/usr/local/include -L$HOME/workspace/rpi/install/usr/local/lib" \
   CXX="$CXX -I$HOME/workspace/rpi/install/usr/local/include -L$HOME/workspace/rpi/install/usr/local/lib" \
   ./configure -C --with-openssl=$HOME/workspace/rpi/install/usr/local --with-openssl-rpath=/usr/local/lib \
     --prefix=/usr/local --host=armv7l-unknown-linux-gnueabihf --build=aarch64-unknown-linux-gnu \
     --with-build-python=/opt/python/3.11.0/bin/python3.11 \
     --enable-optimizations --with-lto --with-computed-gotos --with-system-ffi --disable-ipv6'

make -j9
make install DESTDIR=$HOME/workspace/rpi/install
```

## DBUS
### Local compile
```
TODO
```

### Cross-compile
TODO

## GLIBC (Optional)
### Local compile
```
TODO
```

### Cross-compile
```
x-compile.sh armv8-rpi4-linux-gnueabihf \
  'CHOST=arm ../configure --prefix=/usr/local --host=arm-linux-gnueabihf --disable-sanity-checks'

make -j9
make install DESTDIR=$HOME/workspace/rpi/install
```
