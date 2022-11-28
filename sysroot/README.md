# Sysroot area for Raspberry Pi cross-compilation
This directory is the complementary sysroot area for the cross-compiler. It is added to the include paths alongside those from the cross-compiler itself. area for deployment to Raspberry Pi. This is what the `$X_COMPILE_SYSROOT_PREFIX` environment variable points to.
```
apt download \
  libbz2-1.0 libbz2-dev \
  libexpat1-dev \
  libffi7 libffi-dev \
  libgdbm-compat4 libgdbm-compat-dev \
  libgdbm6 libgdbm-dev \
  liblzma5 liblzma-dev \
  libnsl2 libnsl-dev \
  libreadline8 libreadline-dev \
  libtirpc3 libtirpc-dev \
  libuuid1 uuid-dev \
  zlib1g zlib1g-dev

for i in *.deb; do dpkg-deb --extract $i .; done && rm *.deb
```
