# crosstool-NG toolchain script for Raspberry Pi
Tested against [crosstool-NG](https://github.com/crosstool-ng/crosstool-ng) version 1.25.0. Follow the instructions below to install it and then execute `ct-ng build` in this directory.
```
git clone --depth 1 --branch crosstool-ng-1.25.0 --single-branch https://github.com/crosstool-ng/crosstool-ng.git

sudo apt install \
    autoconf autoconf-archive \
    autopoint \
    bison \
    build-essential \
    cmake \
    flex \
    gawk \
    gettext \
    help2man \
    libbz2-1.0 libbz2-dev \
    libffi8 libffi-dev \
    libgdbm-compat4 libgdbm-compat-dev \
    libgdbm6 libgdbm-dev \
    liblzma5 liblzma-dev \
    libncurses-dev \
    libnsl2 libnsl-dev \
    libreadline8 libreadline-dev \
    libtirpc3 libtirpc-dev \
    libtool-bin \
    libuuid1 uuid-dev \
    patchelf \
    pkg-config \
    python3-tk \
    texinfo \
    xsltproc \
    yacc \
    zlib1g zlib1g-dev

./bootstrap
./configure --prefix=$HOME/.local
make -j11
make install
```
