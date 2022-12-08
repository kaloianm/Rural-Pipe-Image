# Staging area for deployment to Raspberry Pi
This directory constitutes the staging area for deployment to Raspberry Pi. This is what the `$X_COMPILE_STAGING_PREFIX` environment variable points to.

```
dpkg-deb -Zxz -b --root-owner-group RPI-DBus/ .
dpkg-deb -Zxz -b --root-owner-group RPI-Glib/ .
dpkg-deb -Zxz -b --root-owner-group RPI-GlibC/ .
dpkg-deb -Zxz -b --root-owner-group RPI-LibMBIM/ .
dpkg-deb -Zxz -b --root-owner-group RPI-LibQMI/ .
dpkg-deb -Zxz -b --root-owner-group RPI-LibQRTR/ .
dpkg-deb -Zxz -b --root-owner-group RPI-ModemManager/ .
dpkg-deb -Zxz -b --root-owner-group RPI-OpenSSL/ .
dpkg-deb -Zxz -b --root-owner-group RPI-Python3/ .
```

To install:
```
sudo dpkg --install \
  rpi-openssl_3.0.7-RPI_armhf.deb \
  rpi-python3_3.11.0-RPI_armhf.deb \
  rpi-dbus_1.14.4-RPI_armhf.deb \
  rpi-glib_2.56.4-RPI_armhf.deb \
  rpi-libqrtr_1.0.0-RPI_armhf.deb \
  rpi-libmbim_1.26.4-RPI_armhf.deb \
  rpi-libqmi_1.30.8-RPI_armhf.deb \
  rpi-modemmanager_1.18.12-RPI_armhf.deb

Optional (haven't figure out how to get it to work):
  sudo dpkg --install rpi-glibc_3.26-RPI_armhf.deb

sudo ldconfig
```

To uninstall:
```
sudo dpkg --remove rpi-modemmanager rpi-libqmi rpi-libmbim rpi-libqrtr rpi-glib rpi-dbus rpi-python3 rpi-openssl rpi-glibc
```
