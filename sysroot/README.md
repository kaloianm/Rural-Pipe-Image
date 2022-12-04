# Sysroot area for Raspberry Pi cross-compilation
This directory is the complementary sysroot area for the cross-compiler. It is added to the include paths alongside those from the cross-compiler itself. area for deployment to Raspberry Pi. This is what the `$X_COMPILE_SYSROOT_PREFIX` environment variable points to.

Download the following packages on the Raspberry Pi itself (I couldn't figure out how to make `apt get` download packages from a different distribution on the build machine).
```
apt download \
  libblkid1 libblkid-dev \
  libbz2-1.0 libbz2-dev \
  libeditline0 libeditline-dev \
  libelf1 libelf-dev \
  libexpat1 libexpat1-dev \
  libffi7 libffi-dev \
  libgdbm-compat4 libgdbm-compat-dev \
  libgdbm6 libgdbm-dev \
  libgudev-1.0-0 libgudev-1.0-dev \
  liblzma5 liblzma-dev \
  libmount1 libmount-dev \
  libnsl2 libnsl-dev \
  libpcre2-8-0 libpcre2-dev libpcre2-16-0 libpcre2-32-0 libpcre2-posix2 \
  libreadline8 libreadline-dev \
  libselinux1 libselinux1-dev \
  libsepol1 libsepol1-dev \
  libtirpc3 libtirpc-dev \
  libudev1 libudev-dev \
  libuuid1 uuid-dev \
  zlib1g zlib1g-dev
```

Then, on the build machine:
```
pushd $X_COMPILE_SYSROOT_PREFIX

for i in *.deb; do dpkg-deb --extract $i .; done && rm *.deb

ln -sf ../../../lib/arm-linux-gnueabihf/libbz2.so.1.0 usr/lib/arm-linux-gnueabihf/libbz2.so
ln -sf ../../../lib/arm-linux-gnueabihf/libexpat.so.1.6.12 usr/lib/arm-linux-gnueabihf/libexpat.so
ln -sf ../../../lib/arm-linux-gnueabihf/libhistory.so.8 usr/lib/arm-linux-gnueabihf/libhistory.so
ln -sf ../../../lib/arm-linux-gnueabihf/liblzma.so.5.2.5 usr/lib/arm-linux-gnueabihf/liblzma.so
ln -sf ../../../lib/arm-linux-gnueabihf/libreadline.so.8 usr/lib/arm-linux-gnueabihf/libreadline.so
ln -sf ../../../lib/arm-linux-gnueabihf/libselinux.so.1 usr/lib/arm-linux-gnueabihf/libselinux.so
ln -sf ../../../lib/arm-linux-gnueabihf/libsepol.so.1 usr/lib/arm-linux-gnueabihf/libsepol.so
ln -sf ../../../lib/arm-linux-gnueabihf/libtirpc.so.3.0.0 usr/lib/arm-linux-gnueabihf/libtirpc.so
ln -sf ../../../lib/arm-linux-gnueabihf/libz.so.1.2.11 usr/lib/arm-linux-gnueabihf/libz.so

for i in `grep -R ' /usr/local/lib/lib' * | awk -F\: '{ print $1; }' | sort | uniq`; do perl -pi -e 's/\/usr\/local\/lib\/lib/\/home\/parallels\/x-tools\/armv8-RuralPipe-linux-gnueabihf\/armv8-RuralPipe-linux-gnueabihf\/sysroot\/usr\/local\/lib\/lib/g' $i; done

popd
```
