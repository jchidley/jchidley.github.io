---
date: "2020-11-18"
title: "Alpine Linux Raspberry Pi Router"
---

<!-- markdownlint-disable MD025 -->
# Alpine Linux Raspberry Pi Router
<!-- markdownlint-enable MD025 -->

This is a follow up to my earlier posts about building cheap, high performance and flexible home router.

## Instructions

Network addresses will need to be adjusted. Don't forget, that if you're behind a private network, the 'Martian' addresses will need to be adusted in the firewall.

### Basic Setup

see "Alpine Linux Install", need ssh server and the hardware provided Random Number Generator (RNG) Device (hwrng)

Things to change

* alpine-router # hostname
* address 10.2.0.1 # eth1 interface
* chidley.home #local domain name
* dhcp-range=10.2.1.1,10.2.1.255,255.255.0.0,12h # or whatever your local network needs to be

```bash
mount /media/mmcblk0p1 -o rw,remount
apk -U upgrade
```

```bash
# --- rtc ---
cat > $tdir/usercfg.txt << "EOF"
# for the RTC
dtparam=i2c
dtoverlay=i2c-rtc,pcf8523 # ds3231 or pcf8523
EOF
```

```bash
sync # make sure all the files are written to the SD card
umount $tdrive
rmdir $tdrive
```

boot

[Alpine Linux on a Raspberry Pi 3 B+ with a RTC module](http://community.riocities.com/alpine_rpi_rtc.html)

```bash
apk add mkinitfs
```

add `rpirtc` to the end of the features list in /etc/mkinitfs/mkinitfs.conf

rebuild the initial RAM fs image.

```bash
. /etc/lbu/lbu.conf
ln -s /media/$LBU_MEDIA/boot /boot
mount /media/$LBU_MEDIA -o remount,rw
. /etc/mkinitfs/mkinitfs.conf
mkinitfs -F "$features squashfs"
mount /media/$LBU_MEDIA -o remount,ro
```

Enable the hwclock service

boot

```bash
rc-update del swclock boot
rc-update add hwclock boot
hwclock -w
lbu commit
```

```bash
rc-service hwclock start # if you have a RTC with the date already set
date -s 2012011342 # set date to approprite value, e.g. 2020 November 27 13:47
setup-alpine -f answerfile.txt
apk -U upgrade # update and upgrade
apk add dropbear # dropbear not installed
apk add dropbear-dbclient
lbu commit
ip add # get ip address
reboot # belt and braces
```

Dropbear installation is a little buggy, so need to login locally again and check all is OK.

```bash
apk add dropbear
rc-update add dropbear
rc-service dropbear start
lbu ci
```

### OverlayFS

```bash
ssh jack@10.3.151.102 # substitute correct ip address
mkdir /media/mmcblk0p2
echo "/dev/mmcblk0p2 /media/mmcblk0p2 ext4 rw,relatime,errors=remount-ro 0 0" >> /etc/fstab
mount -a
mkdir /media/mmcblk0p2/home
mkdir /media/mmcblk0p2/.workhome
echo "overlay /home overlay lowerdir=/home,upperdir=/media/mmcblk0p2/home,workdir=/media/mmcblk0p2/.workhome 0 0" >> /etc/fstab 
mount -a
df # check overlays are mounted
adduser jack --home /home/jack
lbu ci -d
reboot
```

```bash
ssh jack@10.3.151.102 # substitute correct ip address
su
```

## Router Setup

[Static IP and Network Configuration on Debian Linux](https://www.howtoforge.com/debian-static-ip-address)
[Linux Router with VPN on a Raspber](https://wiki.alpinelinux.org/wiki/Linux_Router_with_VPN_on_a_Raspberry_Pi)
[WireGuard on Alpine Linux with nftables](https://alextsang.net/articles/20191012-080947/index.html)

### Dnsmasq

```bash
# --- dnsmasq ---
apk add dnsmasq
rc-update add dnsmasq
# rc-service dnsmasq start
mv /etc/dnsmasq.conf /etc/dnsmasq.conf.example
cat > /etc/dnsmasq.conf << "EOF"
# --- DNS ---
# Listen on this specific port instead of the standard DNS port
# (53) as ‘unbound’ is the DNS server.
port=35353

# Add local-only domains here, queries in these domains are answered
# from /etc/hosts or DHCP only.
local=/localnet/

# interface _not_ to listen on (WAN)
except-interface=eth0

# Set this (and domain: see below) if you want to have a domain
# automatically added to simple names in a hosts-file.
expand-hosts

# Set the domain for dnsmasq. this is optional, but if it is set, it
# does the following things.
# 1) Allows DHCP hosts to have fully qualified domain names, as long
#     as the domain part matches this setting.
# 2) Sets the "domain" DHCP option thereby potentially setting the
#    domain of all systems configured by list of ports in use on linuxDHCP
# 3) Provides the domain part for "expand-hosts"
domain=chidley.home
# This is small as it covers just local DNS lookup
cache-size=1000

# --- DHCP ---
dhcp-authoritative
interface=br0 # only listen on LAN port
# DHCP range with netmask. This must fit with the
# netmask/ip address assigned to the (static) interface
dhcp-range=10.2.1.1,10.2.1.255,255.255.0.0,12h

# dhcp-leasefile=/var/lib/misc/dnsmasq.leases

# Set the NTP time server address to be the same machine as
# is running dnsmasq
dhcp-option=option:ntp-server,0.0.0.0

# Set the DNS server address to be the same machine as
# is running dnsmasq
dhcp-option=option:dns-server,0.0.0.0

dhcp-option=option:domain-name,chidley.home

# --- PXE ---
EOF
sed -i s/chidley.home/example.com/ /etc/dnsmasq.conf # change example.com
sed -i s/10.2/10.10/g /etc/dnsmasq.conf # change 10.10
lbu ci -d
```

### Unbound

```bash
apk add unbound
rc-update add unbound
rc-service dnsmasq start
rc-service hostapd start
wget https://www.internic.net/domain/named.root -O /etc/unbound/root.hints
#https://kevinlocke.name/bits/2017/03/09/unbound-with-dnsmasq-on-openwrt/
# --- unbound ---
cat > /etc/unbound/unbound.conf << "EOF"
server:
  interface: 0.0.0.0
  interface: ::0
  root-hints: "/etc/unbound/root.hints"
  access-control: 127.0.0.0/8 allow
  access-control: 10.2.0.0/16 allow
  do-not-query-localhost: no
  domain-insecure: "2.10.in-addr.arpa"
  domain-insecure: "chidley.home"
  local-zone: "2.10.in-addr.arpa." nodefault
  private-address: 10.0.0.0/8
  private-address: 169.254.0.0/16
  private-address: 172.16.0.0/12
  private-address: 192.168.0.0/16
  private-address: fd00::/8
  private-address: fe80::/10
  private-domain: "chidley.home"

forward-zone:
  name: "chidley.home"
  forward-addr: 127.0.0.1@35353

forward-zone:
  name: "2.10.in-addr.arpa"
  forward-addr: 127.0.0.1@35353
EOF
sed -i s/chidley.home/example.com/ /etc/unbound/unbound.conf # change example.com
sed -i s/2.10.in-addr.arpa/10.10.in-addr.arpa/g /etc/unbound/unbound.conf # change 10.10.in-addr.arpa
sed -i s/10.2.0.0/10.10.0.0/g /etc/unbound/unbound.conf #  change 10.10.0.0
unbound-checkconf
rc-service unbound start
# use unbound and not google for DNS resolution
# https://www.shellhacks.com/setup-dns-resolution-resoapk add nftableslvconf-example/
sed -i s/8.8.8.8/127.0.0.1/ /etc/resolv.conf 
lbu ci
```

Need hardware random number generator

[The HWRNG on the BCM2838 is compatible to iproc-rng200](https://github.com/raspberrypi/linux/commit/577a2fa60481a0563b86cfd5a0237c0582fb66e0)apk add nftables
[Arch Linux Arm: Raspberry Pi](https://archlinuxarm.org/wiki/Raspberry_Pi)

`haveged` competes with the broadcom provided random number generator, now `iproc-rng200` (previously bcm2835_rng and bcm2708-rng) and so it needs to be disabled

```bash
cat /proc/sys/kernel/random/entropy_avail
# typically less than 1000
apk add rng-tools
RNGD_OPTS="-x1 -o /dev/random -r /dev/hwrng"
rc-service rngd start
rc-update add rngd
cat /proc/sys/kernel/random/entropy_avail
# should be more than 3000
rngd -l
# The "Hardware RNG Device (hwrng)" should be an "Available and enabled entropy source"
lbu ci
```

### Basic Firewall and Routing

This router configuration will forward all traffic between all interfaces.

```bash
# --- forwarding for routing ---
cat > /etc/sysctl.d/local.conf << "EOF"
# Controls IP packet forwarding
net.ipv4.ip_forward = 1
EOF
```

This `nftables` does masquerading so that you can use your internet connection with multiple clients, there is no filtering or traffic management./etc/network/interfaces

```bash
apk add nftables
cat > /etc/nftables.nft << "EOF"
flush ruleset
define wan = eth0
table ip nat {
  chain postrouting {
    type nat hook postrouting priority srcnat;

    oif $wan masquerade persistent
  }
}
EOF
rc-update add nftables
lbu ci
rc-service nftables start
rc-service nftables list # should be as entered above/etc/network/interfaces
reboot
```

Once the above works, then see [Traffic Manager for a better "firewall"](2020-01-07-Traffic-Manager-Not-Firewall.html).

## Wireless Access Point

[Raspberry Pi 3 - Configuring it as wireless access point -AP Mode](https://wiki.alpinelinux.org/wiki/Raspberry_Pi_3_-_Configuring_it_as_wireless_access_point_-AP_Mode)

```bash
apk add hostapd
apk add bridge
rc-update add hostapd
# --- hostapd ---
# https://raspberrypi.stackexchange.com/questions/69866/wlan0-could-not-connect-to-kernel-driver
cat > /etc/hostapd/hostapd.conf << "EOF"
interface=wlan0
bridge=br0
driver=nl80211
ssid=C_test
hw_mode=g
channel=1
macaddr_acl=0
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_passphrase=chidley_secret
rsn_pairwise=CCMP
wpa_pairwise=CCMP
EOF
sed -i s/C_test/C_J/ /etc/hostapd/hostapd.conf # change C_J
sed -i s/chidley_secret/secret/ /etc/hostapd/hostapd.conf # change secret
lbu ci -d
# --- network interfaces ---
cat > /etc/network/interfaces << "EOF"
auto lo
iface lo inet loopback

# Internal Ethernet - WAN
auto eth0
iface eth0 inet dhcp
    hostname alpine-router

auto br0
iface br0 inet static
    bridge-ports wlan0 eth1
    bridge-stp 0
    address 10.2.0.1
    netmask 255.255.0.0
EOF
sed -i s/10.2.0.1/10.10.0.1/ /etc/network/interfaces # change 10.10.0.1
```

```bash
rc-service dnsmasq start
rc-service hostapd start
# to test, then
rc-update add hostapd
rc-update add dnsmasq
lbu ci
```

/etc/network/interfaces### i2c for RTC

* [Saving time with Hardware Clock](https://wiki.alpinelinux.org/wiki/Saving_time_with_Hardware_Clock)
* [How to activate Raspberry-pi’s i2c bus](https://openest.io/en/2020/01/18/activate-raspberry-pi-4-i2c-bus/)
* [Adafruit - Adding a Real Time Clock to Raspberry Pi](https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi/set-up-and-test-i2c)
* [Raspberry Pi Device Trees, overlays, and parameters](https://www.raspberrypi.org/documentation/configuration/device-tree.md#part4.6)

## Dnsmasq and Unbound Links

* [Unbound with Dnsmasq on OpenWrt - Kevin Locke’s Homepage](https://kevinlocke.name/bits/2017/03/09/unbound-with-dnsmasq-on-openwrt/)
* [Combining Dnsmasq and Unbound – Simon Josefsson’s blog](https://blog.josefsson.org/2015/10/26/combining-dnsmasq-and-unbound/)unbound-checkconf
* [dnsmasq + unbound](http://blog.alanporter.com/2014-03-09/dnsmasq-unbound/)
* [Unbound DNS Server Tutorial @ Calomel.org](https://calomel.orgunbound-checkconf/unbound_dns.html)
* [Unbound, an Easy, Fast and Small DNS Resolver](http://troubleshooters.com/linux/unbound_nsd/unbound.htm#authoritative)
* [Use dnsmasq to provide DNS & DHCP services - Fedora Magazine](https://fedoramagazine.org/dnsmasq-provide-dns-dhcp-services/)
* [dnsmasq - Debian Wiki](https://wiki.debian.org/dnsmasq)
* [dnsmasq/dnsmasq.conf.example at master · imp/dnsmasq · GitHub](https://github.com/imp/dnsmasq/blob/master/dnsmasq.conf.example)
* [Lightweight ad-blocking with dnsmasq and Raspberry Pi](https://alexellisuk.medium.com/lightweight-ad-blocking-with-dnsmasq-and-raspberry-pi-665dbb3242e3)
* [Easy Mapping » Linux Magazine](https://www.linux-magazine.com/Issues/2009/101/Dnsmasq)

## Links

* [Nftables/Examples - Gentoo Wiki](https://wiki.gentoo.org/wiki/Nftables/Examples)
* [Scripting - nftables wiki](https://wiki.nftables.org/wiki-nftables/index.php/Scripting)
* [How do I see what iptables is doing?](https://www.opsist.com/blog/2015/08/11/how-do-i-see-what-iptables-is-doing.html)
* [Alpine Linux Stateful Firewall](https://ronvalente.net/posts/alpine-firewall/)
* [Blocking DHCP servers and router advertisements with nftables | ungleich.ch](https://ungleich.ch/u/blog/nftables-block-dhcp-and-router-advertisements/)
* [Linux Router with VPN on a Raspberry Pi (IPv6) - Alpine Linux](https://wiki.alpinelinux.org/wiki/Linux_Router_with_VPN_on_a_Raspberry_Pi_(IPv6))

<!-- markdownlint-disable MD034 -->
https://wiki.alpinelinux.org/wiki/How_to_set_up_Alpine_as_a_wireless_router
https://thepihut.com/blogs/raspberry-pi-tutorials/setting-up-a-wireless-access-point-a-bridge-method-internet-over-wired-ethernet
https://wiki.alpinelinux.org/wiki/Bridge_wlan0_to_eth0

https://unix.stackexchange.com/questions/363332/how-do-i-configure-a-network-interface-bridge-from-wifi-to-ethernet-with-debian

https://www.thegeekstuff.com/2017/06/brctl-bridge/
https://tldp.org/HOWTO/BRIDGE-STP-HOWTO/set-up-the-bridge.html
https://www.raspberrypi.org/documentation/configuration/wireless/access-point-routed.md
<!-- markdownlint-enable MD034 -->
