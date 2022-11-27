# Staging area for deployment to Raspberry Pi
This directory constitutes the staging area for deployment to Raspberry Pi. This is what the `$X_COMPILE_STAGING_PREFIX` environment variable points to.

```
dpkg-deb -Zxz -b RPI-OpenSSL/ .
dpkg-deb -Zxz -b RPI-Python3.11/ .
```
