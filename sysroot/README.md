# Sysroot area for Raspberry Pi cross-compilation
This directory is the complementary sysroot area for the cross-compiler. It is added to the include paths alongside those from the cross-compiler itself. area for deployment to Raspberry Pi. This is what the `$X_COMPILE_SYSROOT_PREFIX` environment variable points to.

Download the following packages on the Raspberry Pi itself (I couldn't figure out how to make `apt get` download packages from a different distribution on the build machine).
```
apt download \
  libblkid1:armhf libblkid-dev:armhf \
  libbz2-1.0:armhf libbz2-dev:armhf \
  libexpat1:armhf libexpat1-dev:armhf \
  libffi7:armhf libffi-dev:armhf \
  libgdbm-compat4:armhf libgdbm-compat-dev:armhf \
  libgdbm6:armhf libgdbm-dev:armhf \
  liblzma5:armhf liblzma-dev:armhf \
  libmount1:armhf libmount-dev:armhf \
  libnsl2:armhf libnsl-dev:armhf \
  libpcre2-8-0:armhf libpcre2-dev:armhf libpcre2-16-0:armhf libpcre2-32-0:armhf libpcre2-posix2:armhf \
  libreadline8:armhf libreadline-dev:armhf \
  libselinux1:armhf libselinux1-dev:armhf \
  libsepol1:armhf libsepol1-dev:armhf \
  libtirpc3:armhf libtirpc-dev:armhf \
  libuuid1:armhf uuid-dev:armhf \
  libelf1:armhf libelf-dev:armhf \
  zlib1g:armhf zlib1g-dev:armhf
```

Then, on the build machine:
```
pushd $X_COMPILE_SYSROOT_PREFIX

for i in *.deb; do \
  dpkg --root $X_COMPILE_SYSROOT_PREFIX \
    --log $X_COMPILE_SYSROOT_PREFIX\dpkg.log \
    --force-not-root \
    --force-architecture \
    --install $i; \
done

rm *.deb

ln -sf ../../../lib/arm-linux-gnueabihf/libbz2.so.1.0 usr/lib/arm-linux-gnueabihf/libbz2.so
ln -sf ../../../lib/arm-linux-gnueabihf/libexpat.so.1.6.12 usr/lib/arm-linux-gnueabihf/libexpat.so
ln -sf ../../../lib/arm-linux-gnueabihf/libhistory.so.8 usr/lib/arm-linux-gnueabihf/libhistory.so
ln -sf ../../../lib/arm-linux-gnueabihf/liblzma.so.5.2.5 usr/lib/arm-linux-gnueabihf/liblzma.so
ln -sf ../../../lib/arm-linux-gnueabihf/libreadline.so.8 usr/lib/arm-linux-gnueabihf/libreadline.so
ln -sf ../../../lib/arm-linux-gnueabihf/libselinux.so.1 usr/lib/arm-linux-gnueabihf/libselinux.so
ln -sf ../../../lib/arm-linux-gnueabihf/libsepol.so.1 usr/lib/arm-linux-gnueabihf/libsepol.so
ln -sf ../../../lib/arm-linux-gnueabihf/libz.so.1.2.11 usr/lib/arm-linux-gnueabihf/libz.so
```
