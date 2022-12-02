# Sysroot area for Raspberry Pi cross-compilation
This directory is the complementary sysroot area for the cross-compiler. It is added to the include paths alongside those from the cross-compiler itself. area for deployment to Raspberry Pi. This is what the `$X_COMPILE_SYSROOT_PREFIX` environment variable points to.
```
apt download \
  libblkid1 libblkid-dev \
  libbz2-1.0 libbz2-dev \
  libexpat1 libexpat1-dev \
  libffi7 libffi-dev \
  libgdbm-compat4 libgdbm-compat-dev \
  libgdbm6 libgdbm-dev \
  liblzma5 liblzma-dev \
  libmount1 libmount-dev \
  libnsl2 libnsl-dev \
  libpcre2-8-0 libpcre2-dev libpcre2-16-0 libpcre2-32-0 libpcre2-posix2 \
  libreadline8 libreadline-dev \
  libselinux1 libselinux1-dev \
  libsepol1 libsepol1-dev \
  libtirpc3 libtirpc-dev \
  libuuid1 uuid-dev \
  libelf1 libelf-dev \
  zlib1g zlib1g-dev

for i in *.deb; do dpkg-deb --extract $i .; done && rm *.deb
```
