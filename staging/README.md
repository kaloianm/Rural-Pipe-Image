# Staging area for deployment to Raspberry Pi
This directory constitutes the staging area for deployment to Raspberry Pi. This is what the `$X_COMPILE_STAGING_PREFIX` environment variable points to.

```
dpkg-deb -Zxz -b --root-owner-group RPI-OpenSSL/ .
dpkg-deb -Zxz -b --root-owner-group RPI-Python3/ .
dpkg-deb -Zxz -b --root-owner-group RPI-DBus/ .
```
