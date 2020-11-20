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

[Install Alpine on a Raspberry Pi](https://wiki.alpinelinux.org/wiki/Raspberry_Pi)
https://wiki.alpinelinux.org/wiki/Classic_install_or_sys_mode_on_Raspberry_Pi

Create an answer file `setup-alpine -c answerfile.txt`

```bash
# Example answer file for setup-alpine script
# If you don't want to use a certain option, then comment it out

# Use US layout with US variant
KEYMAPOPTS="gb gb"

# Set hostname to alpine-router
HOSTNAMEOPTS="-n alpine-router"

# Contents of /etc/network/interfaces
INTERFACESOPTS="auto lo
iface lo inet loopback

# Internal Ethernet
auto eth0
iface eth0 inet dhcp
    hostname alpine-router

# USB Ethernet adapter
auto eth1
iface eth0 inet static
    hostname alpine-router
    address 192.168.1.1
    netmask 255.255.255.0
"

# Search domain of example.com, Google public nameserver
DNSOPTS="-d example.com 8.8.8.8"

# Set timezone to UTC
TIMEZONEOPTS="-z UTC"

# set http/ftp proxy
# PROXYOPTS="http://webproxy:8080"

# Add a random mirror
APKREPOSOPTS="-r"

# Install Dropboar
SSHDOPTS="-c dropbear"

# Use openntpd
NTPOPTS="-c openntpd"

# Use /dev/sda as a data disk
# DISKOPTS="-m data /dev/sda"

# Setup in /media/sdb1
# LBUOPTS="/media/sdb1"
# APKCACHEOPTS="/media/sdb1/cache"
```

```bash
apk update
apk upgrade 
apk add haveged
rc-update add haveged boot
lbu commit -d
service haveged start
reboot
```

## Router Setup

[Static IP and Network Configuration on Debian Linux]https://www.howtoforge.com/debian-static-ip-address)
[Linux Router with VPN on a Raspber](https://wiki.alpinelinux.org/wiki/Linux_Router_with_VPN_on_a_Raspberry_Pi)
[WireGuard on Alpine Linux with nftables](https://alextsang.net/articles/20191012-080947/index.html)


```
apk add nftables
apk add dhcp
```

```bash
cat > /etc/nftables.nft << "EOF"
flush ruleset
table ip nat {
	chain PREROUTING {
		type nat hook prerouting priority filter; policy accept;
	}

	chain POSTROUTING {
		type nat hook postrouting priority srcnat; policy accept;
		ip saddr 192.168.1.0/24 oifname "eth0" masquerade
	}
}
EOF

```bash
cat > /etc/conf.d/dhcpd << "EOF"
# Specify a configuration file - the default is /etc/dhcp/dhcpd.conf
DHCPD_CONF="/etc/dhcp/dhcpd.conf"

# Configure which interface or interfaces to for dhcpd to listen on.
# List all interfaces space separated. If this is not specified then
# we listen on all interfaces.
DHCPD_IFACE="eth0"

# Insert any other dhcpd options - see the man page for a full list.
DHCPD_OPTS="-4"
EOF
```

```bash
cat > /etc/dhcpd.conf << "EOF"
authoritative;
ddns-update-style interim;

option domain-name-servers 8.8.8.8;

shared-network home {
  subnet 192.168.1.0 netmask 255.255.255.0 {
    range 192.168.1.10 192.168.1.240;
    option subnet-mask 255.255.255.0;
    option broadcast-address 192.168.1.255;
    option ntp-servers 192.168.1.1;
    allow unknown-clients;
  }

}
EOF
```

```bash
cat > /etc/sysctl.d/local.conf << "EOF"
# Controls IP packet forwarding
net.ipv4.ip_forward = 1
EOF
```

[The HWRNG on the BCM2838 is compatible to iproc-rng200](https://github.com/raspberrypi/linux/commit/577a2fa60481a0563b86cfd5a0237c0582fb66e0)
[Arch Linux Arm: Raspberry Pi](https://archlinuxarm.org/wiki/Raspberry_Pi)

```
# This competes with the broadcom provided random number generator, now `iproc-rng200` (previously bcm2835_rng and bcm2708-rng)
cat /proc/sys/kernel/random/entropy_avail
# about 1000
service haveged stop
rc-update del haveged boot
apk del haveged
apk add rng-tools
RNGD_OPTS="-x1 -o /dev/random -r /dev/hwrng"
service rngd start
rc-update add rngd default
cat /proc/sys/kernel/random/entropy_avail
# should be more than 3000
rngd -l
# The "Hardware RNG Device (hwrng)" should an "Available and enabled entropy source"
lbu ci -d
```

## Links
* [Nftables/Examples - Gentoo Wiki](https://wiki.gentoo.org/wiki/Nftables/Examples)
* [Scripting - nftables wiki](https://wiki.nftables.org/wiki-nftables/index.php/Scripting)
* [How do I see what iptables is doing?](https://www.opsist.com/blog/2015/08/11/how-do-i-see-what-iptables-is-doing.html)
* [Alpine Linux Stateful Firewall](https://ronvalente.net/posts/alpine-firewall/)
* [Blocking DHCP servers and router advertisements with nftables | ungleich.ch](https://ungleich.ch/u/blog/nftables-block-dhcp-and-router-advertisements/)
* [Linux Router with VPN on a Raspberry Pi (IPv6) - Alpine Linux](https://wiki.alpinelinux.org/wiki/Linux_Router_with_VPN_on_a_Raspberry_Pi_(IPv6))

<!-- markdownlint-enable MD034 -->