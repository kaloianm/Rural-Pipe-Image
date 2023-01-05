# Staging area for deployment to Raspberry Pi
This directory constitutes the staging area for deployment to Raspberry Pi. This is what the `$X_COMPILE_STAGING_PREFIX` environment variable points to.

To generate the Debian packages:
```
dpkg-deb -Zxz -b --root-owner-group RPI-python3.11/ .
dpkg-deb -Zxz -b --root-owner-group RPI-dbus/ .
dpkg-deb -Zxz -b --root-owner-group RPI-libglib2.0/ .
dpkg-deb -Zxz -b --root-owner-group RPI-libmbim-glib/ .
dpkg-deb -Zxz -b --root-owner-group RPI-libqmi-glib/ .
dpkg-deb -Zxz -b --root-owner-group RPI-libqrtr-glib/ .
dpkg-deb -Zxz -b --root-owner-group modemmanager/ .
```

To install the Debian packages:
```
scp \
  rpi-python3.11_3.11.1+RPI_armhf.deb \
  rpi-dbus_1.14.4+RPI_armhf.deb \
  rpi-libglib2.0_2.58.3+RPI_armhf.deb \
  rpi-libmbim-glib_1.26.4+RPI_armhf.deb \
  rpi-libqmi-glib_1.30.8+RPI_armhf.deb \
  rpi-libqrtr-glib_1.0.0+RPI_armhf.deb \
  modemmanager_1.18.12+RPI_armhf.deb \
  <RemoteMachine>:

sudo dpkg --install \
  rpi-python3.11_3.11.1+RPI_armhf.deb \
  rpi-dbus_1.14.4+RPI_armhf.deb \
  rpi-libglib2.0_2.58.3+RPI_armhf.deb \
  rpi-libmbim-glib_1.26.4+RPI_armhf.deb \
  rpi-libqmi-glib_1.30.8+RPI_armhf.deb \
  rpi-libqrtr-glib_1.0.0+RPI_armhf.deb \
  modemmanager_1.18.12+RPI_armhf.deb

sudo ldconfig

sudo python3.11 -m ensurepip
sudo python3.11 -m pip install --upgrade pip setuptools wheel
```

To uninstall:
```
sudo dpkg --remove modemmanager rpi-dbus rpi-libglib2.0 rpi-libmbim-glib rpi-libqmi-glib rpi-libqrtr-glib rpi-python3.11

sudo ldconfig
```
