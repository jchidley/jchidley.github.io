---
date: "2020-11-18"
title: "Alpine Linux Raspberry Pi Router"
---

<!-- markdownlint-disable MD025 -->
# Alpine Linux Raspberry Pi Router
<!-- markdownlint-enable MD025 -->

<!-- markdownlint-disable MD034 -->

This is a follow up to my earlier posts about building cheap, high performance and flexible home router.

## Instructions



### On the Build machine

I am using a raspberry pi running Raspbian OS

[Install Alpine on a Raspberry Pi](https://wiki.alpinelinux.org/wiki/Raspberry_Pi)
https://wiki.alpinelinux.org/wiki/Classic_install_or_sys_mode_on_Raspberry_Pi


We're going to install Alpine in "diskless" mode and use overlay files.  Prepare an SD card with 500MB DOS bootable partition with the remainder as ext4
[Create suitable partitions programatically](https://superuser.com/questions/332252/how-to-create-and-format-a-partition-using-a-bash-script)

```bash
sudo su
export PIDEVICE=/dev/sda # get the correct device from `cat /proc/partitions` or `df -h`
umount ${PIDEVICE}1
umount ${PIDEVICE}2 # many linuxes automount
# clear out old partition
# simulating manual input
# 
# The `sed` script uses the first string of continuous 
# letters and digits after optional spaces, 
# This, in efffect, strips the comments, allowing for in-line comments.
# Note that sending nothing (or spaces) will send a newline
# usually selecting the defaul value.
sed -e 's/\s*\([\+0-9a-zA-Z]*\).*/\1/' << EOF | fdisk ${PIDEVICE}
  o # create a new empty DOS partition table
  w # write table to disk and exit
EOF
sync # make sure that partition table is read by OS
# Create partitions manually using `fdisk` and an "answer file"
sed -e 's/\s*\([\+0-9a-zA-Z]*\).*/\1/' << EOF | fdisk ${PIDEVICE}
  o # create a new empty DOS partition table
  n # new partition
  p # primary partition
  1 # partition number 1
    # default: start at beginning of disk 
  +500M # 500 MB boot parttion
  t # change a partition type
  c # change type of partition to 'W95 FAT32 (LBA)'
  n # add a new partition
  p # primary partition
  2 # partion number 2
    # default: start immediately after preceding partition
    # default: extend partition to end of disk
  p # print the partition table
  w # write table to disk and exit
EOF
```

```bash
mkfs.vfat ${PIDEVICE}1
mkfs.ext2 ${PIDEVICE}2
mkdir /mnt/piboot
mount ${PIDEVICE}1 /mnt/piboot
```

To find out the correct options, run `setup-alpine -c answerfile.txt` on a newly booted Alpine system.

```bash
cat > /mnt/piboot/answerfile.txt << "EOF"
# Use GB layout with GB variant
KEYMAPOPTS="gb gb"

# Set hostname to alpine-router
HOSTNAMEOPTS="-n alpine-router.home"

# Contents of /etc/network/interfaces
INTERFACESOPTS="auto lo
iface lo inet loopback

# Internal Ethernet
auto eth0
iface eth0 inet dhcp
    hostname alpine-router

# USB Ethernet adapter
auto eth1
iface eth1 inet static
    hostname alpine-router.home
    address 192.168.10.1
    netmask 255.255.255.0
"

# `home` is the local domain name and 8.8.8.8 Google public nameserver
# This will be replaced with custom DNS setup
DNSOPTS="-d home -n 8.8.8.8"

# Set timezone to UTC
TIMEZONEOPTS="-z UTC"

# set http/ftp proxy
PROXYOPTS="none"

# Use the first mirror, usually CDN (Content Delivery Network)
APKREPOSOPTS="-1"

# Install Dropboar
SSHDOPTS="-c dropbear"

# Use chronyd
NTPOPTS="-c chrony"

# Setup in /media/mmcblk0p1
LBUOPTS="/media/mmcblk0p1"
APKCACHEOPTS="/media/mmcblk0p1/cache"
EOF
```

```bash
tar -xvf /home/pi/Downloads/alpine-rpi-3.12.1-aarch64.tar.gz -C /mnt/piboot --no-same-owner
```

```bash
cat > /mnt/piboot/usercfg.txt << "EOF"
# for the RTC
dtparam=i2c
dtoverlay=i2c-rtc,pcf8523
EOF
```

```bash
sync
umount ${PIDEVICE}1
umount ${PIDEVICE}2
```

boot

```bash
date -s 2012011342 # set date to approprite value, e.g. 2020 November 27 13:47
rc-service hwclock start # if you have a RTC with the date already set
setup-alpine -f /media/mmcblk0p1/answerfile.txt
apk update
apk upgrade
apk add dropbear # dropbear not installed
rc-update add hwclock # if you have added an RTC
lbu commit -d # delete any previous commits
ip add # get ip address
reboot # belt and braces
```

```bash
ssh root@10.3.151.102
mkdir /media/mmcblk0p2
echo "/dev/mmcblk0p2 /media/mmcblk0p2 ext4 rw,relatime,errors=remount-ro 0 0" >> /etc/fstab
mount -a
mkdir /media/mmcblk0p2/home
mkdir /media/mmcblk0p2/.workhome
mkdir /media/mmcblk0p2/var
mkdir /media/mmcblk0p2/.workvar
echo "overlay /home overlay lowerdir=/home,upperdir=/media/mmcblk0p2/home,workdir=/media/mmcblk0p2/.workhome 0 0" >> /etc/fstab 
echo "overlay /var overlay lowerdir=/var,upperdir=/media/mmcblk0p2/var,workdir=/media/mmcblk0p2/.workvar 0 0" >> /etc/fstab 
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

[Static IP and Network Configuration on Debian Linux]https://www.howtoforge.com/debian-static-ip-address)
[Linux Router with VPN on a Raspber](https://wiki.alpinelinux.org/wiki/Linux_Router_with_VPN_on_a_Raspberry_Pi)
[WireGuard on Alpine Linux with nftables](https://alextsang.net/articles/20191012-080947/index.html)


### Basic Firewall and Routing

This router configuration will forward all traffic between all interfaces.

```bash
cat > /etc/sysctl.d/local.conf << "EOF"
# Controls IP packet forwarding
net.ipv4.ip_forward = 1
EOF
```

```bash
apk add nftables
```

This `nftables` does masquerading so that you can use your internet connection with multiple clients, there is no filtering or traffic management.

```bash
cat > /etc/nftables.nft << "EOF"
flush ruleset
table ip nat {
	chain POSTROUTING {
		type nat hook postrouting priority srcnat; policy accept;
		ip saddr 192.168.10.0/24 oifname "eth0" masquerade
	}
}
EOF
rc-update add nftables
lbu ci -d
rc-service nftables list # after reboot to see that it's working
```

### Dnsmasq

```bash
apk add dnsmasq
rc-update add dnsmasq
lbu ci -d
# rc-service dnsmasq start
mv /etc/dnsmasq.conf /etc/dnsmasq.conf.example
cat > /etc/dnsmasq.conf << "EOF"
# --- DNS
# Never forward plain names (without a dot or domain part)
domain-needed
# Never forward addresses in the non-routed address spaces.
bogus-priv

# Listen on this specific port instead of the standard DNS port
# (53) as DNS service is provied by unbound. 
port=5353

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
#    domain of all systems configured by DHCP
# 3) Provides the domain part for "expand-hosts"
domain=chidley.home

# This only needs to be small as we're only doing local DNS
cache-size=1000

# --- DHCP

dhcp-authoritative
interface=eth1 # only listen on LAN port

# DHCP range with netmask
dhcp-range=192.168.10.50,192.168.10.150,255.255.255.0,12h

# dhcp-leasefile=/var/lib/dnsmasq.leases

# reserved names and addressesserver:
	do-not-query-localhost: no
	domain-insecure: "0.168.192.in-addr.arpa"
	domain-insecure: "example.local"
	local-zone: "168.192.in-addr.arpa." nodefault
	private-address: 10.0.0.0/8
	private-address: 169.254.0.0/16
	private-address: 172.16.0.0/12
	private-address: 192.168.0.0/16
	private-address: fd00::/8
	private-address: fe80::/10
	private-domain: "example.local"
forward-zone:
	name: "example.local"
	forward-addr: 127.0.0.1@53535
forward-zone:
	name: "0.168.192.in-addr.arpa"
	forward-addr: 127.0.0.1@53535
dhcp-host=dc:a6:32:dd:4c:72,pi400-1,192.168.10.20,10m

# Set the NTP time server address to be the same machine as
# is running dnsmasq
dhcp-option=42,0.0.0.0

# --- PXE
EOF
```

### Unbound

```bash
apk add unbound
rc-update add unbound
lbu ci -d
```

```bash
#https://kevinlocke.name/bits/2017/03/09/unbound-with-dnsmasq-on-openwrt/
cat > /etc/unbound/unbound.conf << "EOF"
server:
	do-not-query-localhost: no
	domain-insecure: "10.168.192.in-addr.arpa"
	domain-insecure: "chidley.home"
	local-zone: "168.192.in-addr.arpa." nodefault
	private-address: 10.0.0.0/8
	private-address: 169.254.0.0/16
	private-address: 172.16.0.0/12
	private-address: 192.168.0.0/16
	private-address: fd00::/8
	private-address: fe80::/10
	private-domain: "chidley.home"
forward-zone:
	name: "chidley.home"
	forward-addr: 127.0.0.1@5353
forward-zone:
	name: "10.168.192.in-addr.arpa"
	forward-addr: 127.0.0.1@5353
EOF
lbu ci -d
```


### hardware random number generator

[The HWRNG on the BCM2838 is compatible to iproc-rng200](https://github.com/raspberrypi/linux/commit/577a2fa60481a0563b86cfd5a0237c0582fb66e0)
[Arch Linux Arm: Raspberry Pi](https://archlinuxarm.org/wiki/Raspberry_Pi)

`haveged` competes with the broadcom provided random number generator, now `iproc-rng200` (previously bcm2835_rng and bcm2708-rng) and so it needs to be disabled

```
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
lbu ci -d
```

### i2c for RTC

[Saving time with Hardware Clock](https://wiki.alpinelinux.org/wiki/Saving_time_with_Hardware_Clock)

[How to activate Raspberry-pi’s i2c bus](https://openest.io/en/2020/01/18/activate-raspberry-pi-4-i2c-bus/)

[Adafruit - Adding a Real Time Clock to Raspberry Pi](https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi/set-up-and-test-i2c)

[Raspberry Pi Device Trees, overlays, and parameters](https://www.raspberrypi.org/documentation/configuration/device-tree.md#part4.6)


[Enable Community Repository](https://wiki.alpinelinux.org/wiki/Enable_Community_Repository) by uncommenting the correct line in `/etc/apk/repositories` and then `apk update`. Then you can install `apk i2c-tools` and run the various i2c utilities.



## Dnsmasq and Unbound Links

* [Unbound with Dnsmasq on OpenWrt - Kevin Locke’s Homepage](https://kevinlocke.name/bits/2017/03/09/unbound-with-dnsmasq-on-openwrt/)
* [Combining Dnsmasq and Unbound – Simon Josefsson’s blog](https://blog.josefsson.org/2015/10/26/combining-dnsmasq-and-unbound/)
* [dnsmasq + unbound](http://blog.alanporter.com/2014-03-09/dnsmasq-unbound/)
* [Unbound DNS Server Tutorial @ Calomel.org](https://calomel.org/unbound_dns.html)
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

<!-- markdownlint-enable MD034 -->