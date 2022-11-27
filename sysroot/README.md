# Sysroot area for Raspberry Pi cross-compilation
This directory is the complementary sysroot area for the cross-compiler. It is added to the include paths alongside those from the cross-compiler itself. area for deployment to Raspberry Pi. This is what the `$X_COMPILE_SYSROOT_PREFIX` environment variable points to.
```
apt download libbz2-dev libtirpc-dev libgdbm-dev libreadline-dev lzma-dev lzma
for i in *.deb; do dpkg-deb --extract $i .; done
```
