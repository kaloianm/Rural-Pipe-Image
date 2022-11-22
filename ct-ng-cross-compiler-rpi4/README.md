# crosstool-NG toolchain script for Raspberry Pi
Tested against [crosstool-NG](https://github.com/crosstool-ng/crosstool-ng) version 1.25.0. Follow the instructions below to install it and then execute `ct-ng build` in this directory.
```
git clone --depth 1 --branch crosstool-ng-1.25.0 --single-branch https://github.com/crosstool-ng/crosstool-ng.git

sudo apt install build-essential autoconf flex texinfo help2man gawk libtool-bin libncurses-dev bison yacc
./bootstrap
./configure --prefix=$HOME/.local
make -j9
make install
```
