#!/usr/bin/env python3
#

# Copyright 2022 Kaloian Manassiev
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import argparse
import fileinput
import os
import shlex
import subprocess

if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.\n"
         "Please try again, this time using 'sudo'. Exiting.")

# List of interfaces that we will support
WAN = 'eth0'
MOBILEWAN = 'wwan0'
USBWAN = 'usb0'
LAN = ['eth1', 'eth2']
WLAN24GHZ = 'wlan0'
TUNNEL = ['rpic', 'tun0']

parser = argparse.ArgumentParser(description="""
This script performs all the necessary configuration steps for a clean-installed Raspberry Pi 4
device running Raspbian to be able to serve as a RuralPipe router. Recommended steps before running
it is to 'sudo apt update/upgrade' the installation to the latest packages.
""")
parser.add_argument('wifi_password', help='Password to set on the WiFi hotstpot')
options = parser.parse_args()


# Executes a single shell command and raises an exception containing the command itself and the
# code if it fails.
def shell_command(command):
    err_code = os.system(command)
    if err_code != 0:
        raise Exception(f'Command failed with code {err_code}: {command}')


# Rewrites the entire content of file_name with contents. If 'executable_clause' is not set to None,
# it must contain a string like '#!/bin/sh', which indicates that the file should be an executable.
def rewrite_config_file(file_name, executable_clause, contents):
    file_name_for_backup = file_name + '.rural-pipe.orig'
    shell_command(f'[ ! -f {file_name} ] || cp {file_name} {file_name_for_backup}')

    with open(file_name, 'wt') as file:
        if executable_clause is not None:
            file.write(f'{executable_clause}')

        file.write(f"""
###################################################################################################
# THIS FILE {file_name} WAS AUTO GENERATED BY RuralPipe's configure_client.py SCRIPT
#
# DO NOT EDIT
###################################################################################################
{contents}""")

    if executable_clause is not None:
        st = os.stat(file_name)
        os.chmod(file_name, st.st_mode | 0o111)


# Takes an option of the form 'option_name=option_value' and either updates it in the configuration
# file file_name or adds it if it doesn't exist.
def set_config_option(file_name, option):
    (option_name, option_value) = option.split('=')

    at_first_line = True
    option_set = False

    with fileinput.input(file_name, inplace=True) as file_name_input:
        for input_line in file_name_input:
            if at_first_line and (not 'configure_client.py' in input_line):
                print(
                    f"# THIS FILE {file_name} WAS MODIFIED BY RuralPupe's configure_client.py SCRIPT"
                )
            at_first_line = False
            if option_name in input_line:
                input_line = f'{option_name}={option_value}\n'
                option_set = True
            print(input_line, end='')

    if at_first_line or not option_set:
        with open(file_name, 'a') as file_name_input:
            if at_first_line:
                file_name_input.write(
                    f"# THIS FILE {file_name} WAS MODIFIED BY RuralPupe's configure_client.py SCRIPT"
                )
            if not option_set:
                file_name_input.write(f'{option_name}={option_value}')


# If `line` doesn't exist in `file_name`, adds it at the end, otherwise does nothing.
def append_config_line(file_name, line):
    at_first_line = True
    line_set = False

    with fileinput.input(file_name, inplace=True) as file_name_input:
        for input_line in file_name_input:
            if at_first_line and (not 'configure_client.py' in input_line):
                print(
                    f"# THIS FILE {file_name} WAS MODIFIED BY RuralPupe's configure_client.py SCRIPT"
                )
            at_first_line = False
            if line == input_line:
                line_set = True
            print(input_line, end='')

    if at_first_line or not line_set:
        with open(file_name, 'a') as file_name_input:
            if at_first_line:
                file_name_input.write(
                    f"# THIS FILE {file_name} WAS MODIFIED BY RuralPupe's configure_client.py SCRIPT"
                )
            if not line_set:
                file_name_input.write(line)


# 0. Recommended first (manual) step after installing Raspbian is to run sudo apt update in order
# to obtain the latest versions of all packages.


# 1. Check the list of available network interfaces contains at least the WAN, MOBILEWAN, LAN and
# WLAN24GHZ interfaces that the rest of the script depends on.
#
# The USBWAN interface is hot-plug, so it won't be checked
def check_network_interfaces():
    p = subprocess.Popen(shlex.split('ifconfig -a -s'), stdout=subprocess.PIPE,
                         universal_newlines=True)
    lines = p.stdout.readlines()
    if not lines[0].startswith('Iface'):
        raise Exception('Unexpected output: ', lines[0])
    interfaces = list(map(lambda itf: itf.split()[0], lines[1:]))
    if not set([WAN]).issubset(set(interfaces)):
        raise Exception('Unable to find the required WAN interfaces')
    if not set([MOBILEWAN]).issubset(set(interfaces)):
        print('WARNING: No WWAN interfaces found')
    if not set([WLAN24GHZ]).issubset(set(interfaces)):
        raise Exception('Unable to find the required LAN interfaces')
    if not set(LAN).issubset(set(interfaces)):
        print('WARNING: No LAN interfaces found')


check_network_interfaces()

# 1. Install the required packages
# yapf: disable
shell_command(
    'echo iptables-persistent iptables-persistent/autosave_v4 boolean true | sudo debconf-set-selections'
)
shell_command(
    'echo iptables-persistent iptables-persistent/autosave_v6 boolean true | sudo debconf-set-selections'
)
shell_command(
    'apt update'
)
shell_command(
    'apt install -y vim screen dnsmasq hostapd netfilter-persistent iptables-persistent bridge-utils openvpn libqmi-utils udhcpc ifmetric snapd net-tools rfkill'
)
# yapf: enable

# 2. Unblock the WLAN device(s) so they can transmit.
shell_command('rfkill unblock wlan')

# 3. Create the LAN bridge interface (WLAN will automatically be added to it when the HostAPD daemon
# starts up).
rewrite_config_file(
    '/etc/network/interfaces', None, f"""
auto lo
iface lo inet loopback

auto {WAN}
iface {WAN} inet dhcp
  metric 10

allow-hotplug {USBWAN}
iface {USBWAN} inet dhcp
  metric 20

manual {MOBILEWAN}
iface {MOBILEWAN} inet manual
  metric 30

{''.join(map(lambda ifname: f'iface {ifname} inet manual' + chr(10), LAN + [WLAN24GHZ]))}

auto br0
iface br0 inet static
  bridge_ports {''.join(map(lambda ifname: f'{ifname} ', LAN))}
  address 192.168.4.1
  broadcast 192.168.4.255
  netmask 255.255.255.0
  bridge_stp 0
  """)

rewrite_config_file(
    f'/etc/udhcpc/{MOBILEWAN}.script', '#!/bin/sh', f"""
RESOLV_CONF="/etc/resolv.conf"

log() {{
    logger -t "udhcpc[$PPID]" -p daemon.$1 --stderr "$interface: $2"
}}

case $1 in
    bound|renew)
    [ -z "$router" ] \\
        && log err "Should be invoked from udhcpc" && exit 1
    [ ! -x "/sbin/resolvconf" ] \\
        && log err "Resolvconf is required" && exit 1

    ifconfig $interface ${{mtu:+mtu $mtu}} $ip netmask $subnet ${{broadcast:+broadcast $broadcast}}
    ip -4 route flush exact 0.0.0.0/0 dev $interface

    [ ".$subnet" = .255.255.255.255 ] \\
        && onlink=onlink || onlink=
    ip -4 route add default via $router dev $interface $onlink

    [ -n "$domain" ] \\
        && R="domain $domain" || R=""
    for i in $dns; do
        R="$R
nameserver $i"
    done

    echo "$R" | resolvconf -a "$interface.udhcpc"

    log info "$1: IP=$ip/$subnet hostname=$hostname router=$router domain=$domain dns=$dns lease=$lease"
    ;;

    deconfig)
    ip link set $interface up
    ip -4 addr flush dev $interface
    ip -4 route flush dev $interface
    resolvconf -d "$interface.udhcpc"

    log notice "$1: Completed"
    ;;

    leasefail | nak)
    log err "$1: Configuration failure: $message"
    ;;

    *)
    log err "$1: Unknown command"
    exit 1
    ;;
esac
""")

rewrite_config_file(
    f'/etc/network/if-pre-up.d/pre-up-{MOBILEWAN}', '#!/bin/sh', f"""
if [ "$IFACE" != "{MOBILEWAN}" ]; then
  exit 0
fi

ifconfig $IFACE down

MODEM_PATH=`mmcli --list-modems | awk '{{ print $1; }}'`
MODEM_ID=`echo "$MODEM_PATH" | awk -F'/' '{{ print $6; }}'`

echo "Found modem $MODEM_ID at $MODEM_PATH"

mmcli -m $MODEM_ID --enable
mmcli -m $MODEM_ID --simple-connect='apn=telefonica.es,user=telefonica,password=telefonica'

PIDFILE="/tmp/udhcpc-{MOBILEWAN}.pid"
udhcpc -i $IFACE --pidfile="$PIDFILE" --script="/etc/udhcpc/{MOBILEWAN}.script"
""")

rewrite_config_file(
    f'/etc/network/if-post-down.d/post-down-{MOBILEWAN}', '#!/bin/sh', f"""
if [ "$IFACE" != "{MOBILEWAN}" ]; then
  exit 0
fi

MODEM_PATH=`mmcli --list-modems | awk '{{ print $1; }}'`
MODEM_ID=`echo "$MODEM_PATH" | awk -F'/' '{{ print $6; }}'`

echo "Found modem $MODEM_ID at $MODEM_PATH"

mmcli -m $MODEM_ID --simple-disconnect
mmcli -m $MODEM_ID --disable

PIDFILE="/tmp/udhcpc-{MOBILEWAN}.pid"
[ -f "$PIDFILE" ] && kill -9 `cat $PIDFILE`
ifconfig $IFACE down
""")

# 4. Configure the DNS/DHCP server
rewrite_config_file(
    '/etc/dnsmasq.conf', None, f"""
interface=br0
dhcp-range=br0,192.168.4.10,192.168.4.200,255.255.255.0,12h

# BEGIN: Fixed IP hosts
#
# To list all the active leases use the following command:
#   cat /var/lib/misc/dnsmasq.leases
#
dhcp-host=b0:4e:26:85:04:0c,192.168.4.10    # TP-Link Archer C9 Router (Salon)
dhcp-host=c0:c9:e3:e2:c4:e1,192.168.4.11    # TP-Link AC750 Router (TV Room)
dhcp-host=f0:18:98:3d:4e:95,192.168.4.12    # Macbook Pro 2017 (Jocelyn's Wifi)
dhcp-host=bc:d0:74:0d:4d:01,192.168.4.13    # Macbook Pro 2021 (Kal's Wifi)
dhcp-host=a4:ae:12:26:22:16,192.168.4.14    # ThinkVision Monitor (Kal's Monitor)
dhcp-host=40:4e:36:93:73:36,192.168.4.15    # Pixel 2 (Kal)
dhcp-host=0c:c4:13:13:93:1b,192.168.4.16    # Pixel 6 (Kal)
#
# END: Fixed IP hosts

domain=rural

dhcp-authoritative

server=8.8.8.8
server=8.8.4.4
    """)

# 5. Configure and enable the hostapd daemon
rewrite_config_file(
    '/etc/hostapd/hostapd.conf', None, f"""
interface={WLAN24GHZ}
bridge=br0

hw_mode=a
channel=36
ieee80211d=1
country_code=FR
ieee80211ac=1
wmm_enabled=1

ssid=RuralPipe (Kitchen)
# 1=wpa, 2=wep, 3=both
auth_algs=1
# WPA2 only
wpa=2
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
wpa_passphrase={options.wifi_password}""")

set_config_option('/etc/default/hostapd', 'DAEMON_CONF="/etc/hostapd/hostapd.conf"')
set_config_option('/etc/default/hostapd', 'DAEMON_OPTS="-f /var/log/hostapd.log"')

shell_command('sudo systemctl unmask hostapd')
shell_command('sudo systemctl enable hostapd')

# 6. Enable IP forwarding, NAT and the special routing rule for the rpi interface
set_config_option('/etc/sysctl.conf', 'net.ipv4.ip_forward=1')

for intf in [WAN, USBWAN, MOBILEWAN] + TUNNEL:
    shell_command(f'iptables -t nat -A POSTROUTING -o {intf} -j MASQUERADE')
shell_command('netfilter-persistent save')

append_config_line('/etc/iproute2/rt_tables', '1    rpi')

# 7. Manual instructions for using OpenVPN with NordVPN
#
# TODO: Automate these instructions
#
# Follow the manual (OpenVPN) instructions at this link:
#   https://support.nordvpn.com/Connectivity/Linux/1047409422/How-can-I-connect-to-NordVPN-using-Linux-Terminal.htm
#
# Create a file with the NordVPN credentials as `$HOME/.nordvpn_cred`: First line is the user name,
# second line is the password.
#
# Connect using the following command line:
#   `sudo openvpn --config /etc/openvpn/ovpn_udp/es63.nordvpn.com.udp.ovpn --auth-user-pass $HOME/.nordvpn_cred`.
