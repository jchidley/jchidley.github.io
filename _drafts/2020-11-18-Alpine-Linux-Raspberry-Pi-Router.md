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

To get the block size of disks `blockdev --getsz /dev/sda`.  The smallest 2GB SD Card that I own is 3840000 512 byte blocks in size.  This should be the aim for an ARM installation so that it easily fits into a 2GB card.

DOS partition a disk, +100M boot, `last sector` 3840000 for root.
mount both, extract archive to root.  Move boot/* to the root of boot partition.

```bash
mkfs.vfat /dev/sdX1
mkdir boot
mount /dev/sdX1 boot
mkfs.ext4 /dev/sdX2
mkdir root
mount /dev/sdX2 root
wget http://os.archlinuxarm.org/os/ArchLinuxARM-rpi-4-latest.tar.gz
bsdtar -xpf ArchLinuxARM-rpi-4-latest.tar.gz -C root
sync
mv root/boot/* boot
```

To get progress of sync run `watch -d grep -e Dirty: -e Writeback: /proc/meminfo`

boot

```bash
pacman-key --init
pacman-key --populate archlinuxarm
```

It is possible to configure a simple router based on the [Arch Linux Router](https://wiki.archlinux.org/index.php/Router) instructions.  I will be going further and installing the software that runs the internet, including the newer firewall nftable.

install the packages

```bash
pacman -S nftables dhcp usbutils
```

```bash
useradd -m -G wheel,audio jack -s /bin/bash
passwd jack
visudo # uncomment "%wheel ALL=(ALL) NOPASSWD: ALL"
userdel -r alarm # after reboot
```

## Setup The Network Connections

This is how identified my USB device.

```bash
lsusb > lsusb.out # then insert the USB ethernet
lsusb | diff lsusb.out - # will display USB ethernet, say AX88179. "-" is for standard input
dmesg | grep AX88179 #AX88179 from above to check that device loaded correctly
ip addr #interface names and MAC addresses
```

I gave my Ethernet devices [known-and-consistent-despite-booting name](https://wiki.archlinux.org/index.php/Systemd-networkd#Renaming_an_interface) to save time troubleshooting, using the MAC addresses from above.

/etc/systemd/network/10-ethusb0.link

```bash
cat > /etc/systemd/network/10-ethusb0.link << "EOF"
[Match]
MACAddress=12:34:56:78:90:ab

[Link]
Description=USB to Ethernet Adaptor
Name=ethusb0
EOF
```

```bash
cat > /etc/systemd/network/11-wan0.link << "EOF"
[Match]
MACAddress=12:34:56:78:90:ab

[Link]
Description=On Board Ethernet
Name=wan0
EOF
```

I called the other one `11-wan0.link`. Each interface has an associated profile.

```bash
cat > /etc/systemd/network/wan0.network << "EOF"
[Match]
Name=wan0

[Network]
DHCP=yes
DNSSEC=no
EOF
```

I chose `10.2.0.0` for my private network and `/16` gives enough device addresses.

```bash
cat > /etc/systemd/network/ethusb0.network << "EOF"
[Match]
Name=ethusb0

[Address]
Address=10.2.0.1

[Network]
DNSSEC=no
EOF
```

enable systemd network service with `systemctl enable systemd-networkd.service`.

A reboot (not forgeting `userdel -r alarm` to remove this well known user) is the quickest way to reset things and ensure that they start correctly at power on.  `ip addr` shows that both interfaces are up and have assigned addresses.

## Routing Between networks

Test forwarding between ip4 networks with `sysctl net.ipv4.ip_forward=1` and then make it permanent with:

```bash
cat > /etc/sysctl.d/30-ipforward.conf << "EOF"
net.ipv4.ip_forward=1
net.ipv6.conf.default.forwarding=1
net.ipv6.conf.all.forwarding=1
EOF
```

## Setting up nftables

I have a private network with a single globally visible IP address provided by the ISP.  I need to share that address with all of my devices internally using `masquerade`.  `nftables`, which is the new replacement for `iptables` (and similar) does this.

Don't forget to set a device the other side with a suitable static IP address (say `10.1.0.2`) and a router name of `10.1.0.1` to test the connection.

`mv  /etc/nftables.conf /etc/nftables.conf.bak` and follow the instructions on the Arch Wiki for [nftables.conf](https://wiki.archlinux.org/index.php/nftables) for simple sharing of a public internet address.

```bash
cat > /etc/nftables.conf << "EOF"
flush ruleset
define wan_if = "wan0"
table ip nat_table {
        chain postrouting {
                type nat hook postrouting priority 0; policy accept;
                oifname $wan_if masquerade
        }
}
EOF
```

Run these commands...

```bash
nft -f /etc/nftables.conf
nft -s list ruleset # check rules have been loaded correctly
systemctl enable nftables
systemctl start nftables
```

and bingo!  A fully functioning Internet router.

I implemented a simple ["firewall"](2020-01-07-Traffic-Manager-Not-Firewall).

## Serving IP Addresses

It is possible to enter every single device's IP settings manually but that is tiresome. 
[Dhcpd](https://wiki.archlinux.org/index.php/Dhcpd) to the rescue.  

Nothing clever here: just following the instructions.  I'm using Google's DNS servers but there are many alternatives like the ISP's.

`mv /etc/dhcpd.conf /etc/dhcpd.conf.bak`

```bash
cat > /etc/dhcpd.conf << "EOF"
# No DHCP service in DMZ network (192.168.2.0/24)
subnet 192.168.2.0 netmask 255.255.255.0 {
}

option domain-name-servers 8.8.8.8;
option subnet-mask 255.255.0.0;
option routers 10.2.0.1;
subnet 10.2.0.0 netmask 255.255.0.0 {
  range 10.2.1.1 10.2.200.250;
}
EOF
```

enable dhcpd on a single interface

```bash
cat > /etc/systemd/system/dhcpd4@.service << "EOF"
[Unit]
Description=IPv4 DHCP server on %I
Wants=network-online.target
After=network-online.target

[Service]
Type=forking
PIDFile=/run/dhcpd4.pid
ExecStart=/usr/bin/dhcpd -4 -q -pf /run/dhcpd4.pid %I
KillSignal=SIGINT

[Install]
WantedBy=multi-user.target
EOF
```

```bash
systemctl enable dhcpd4@ethusb0.service
systemctl start dhcpd4@ethusb0.service
systemctl status dhcpd4@ethusb0.service # will also display the allocated addresses
```

## The End of the Beginning

This is enough to replace the original [pretty-good-for-a-consumer-grade](https://www.asus.com/Networking/RTN66U/) which has been repurposed as a [WAP](https://en.wikipedia.org/wiki/Wireless_access_point).  To exercise more control over the home network requires [implementing a DNS server](2020-01-08-DNS-Setup-For-DIY-Home-Router).

## Links
* [BigDinosaur Blog on Running BIND9 and ISC-DHCP](https://blog.bigdinosaur.org/running-bind9-and-isc-dhcp/)
* [The Ars guide to building a Linux router from scratch](https://arstechnica.com/gadgets/2016/04/the-ars-guide-to-building-a-linux-router-from-scratch/)
* [Getting Gigabit Networking on a Raspberry Pi 2, 3 and B+](https://www.jeffgeerling.com/blogs/jeff-geerling/getting-gigabit-networking)
* [Pi4 Firmware solves overheating driven throtteling](https://www.jeffgeerling.com/blog/2019/raspberry-pi-4-might-not-need-fan-anymore)
* [Arch Linux Router](https://wiki.archlinux.org/index.php/Router)
* [Renaming an interface](https://wiki.archlinux.org/index.php/Systemd-networkd#Renaming_an_interface)
* [Why nftables?](https://wiki.nftables.org/wiki-nftables/index.php/Why_nftables%3F)
* [Arch Linux nftables](https://wiki.archlinux.org/index.php/nftables)
* [Dhcpd](https://wiki.archlinux.org/index.php/Dhcpd)

<!-- markdownlint-enable MD034 -->