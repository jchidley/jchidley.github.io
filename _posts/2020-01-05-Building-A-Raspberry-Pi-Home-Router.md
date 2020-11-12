---
date: "2020-01-05"
title: "Building A Raspberry Pi Home Router"
---

# Building A Raspberry Pi Home Router
Replacing a home router with a Raspberry Pi - better performance and full linux customisation.  Inspired by [bigdinousaur](https://blog.bigdinosaur.org/running-bind9-and-isc-dhcp/) and [Ars Technica](https://arstechnica.com/gadgets/2016/04/the-ars-guide-to-building-a-linux-router-from-scratch/).

## Introduction

I've used a number of home routers over the years and they've worked OK but the performance has been lacklustre, and the configuration options limited.  I wanted to build myself something that I had complete control over and, as a bonus, would teach me more about linux routing.  I stumbled across an [Ars Technica article](https://arstechnica.com/gadgets/2016/04/the-ars-guide-to-building-a-linux-router-from-scratch/) where they did that.  I wanted a minimal build to help with performance, security and power consumption.  Arch linux seemed like a good choice.

I had originally wanted to use a Raspberry Pi 3 (the latest available) as they are dirt cheap, low power a very small.  But my local Internet ISP is Virgin media and the Pi wouldn't be able to support a throughput of up to 200Mbs.  So I looked for cheap low power, low cost, all-in-one, silent Intel devices.  I found a pair identical Shuttle boxes cheaply on eBay; then I would have a swap in backup - nothing is more mission critical for a family than an internet connection.  In the end I only set up one because it was more involved than expected.

With the release of the Raspberry Pi 4 it was time to revisit my solution.  I use a 4GB Pi 4 as a desktop and it will support up to about [900Mbps](https://www.jeffgeerling.com/blogs/jeff-geerling/getting-gigabit-networking).  Changing to a DIY server and good WiFi has demonstrated that a 100Mbps ISP link is good enough, even for a family of 5.  Now is a good time to revisit my work, learn how to setup my router reliably and quickly.  Given Jeff's performance numbers, I expect that my Pi 3 B+ should be good enough, certainly a Pi 4 should do the trick.  I have quite a few old Pis lying around (I love that they maintain compatibility with the old hardware) so if my router goes down I can run the router on an old Pi until a new Pi 4 (or 5!) arrives.

From Jeff Geerling's blog [Getting Gigabit Networking on a Raspberry Pi 2, 3 and B+](https://www.jeffgeerling.com/blogs/jeff-geerling/getting-gigabit-networking).  "You can get Gigabit networking working on any current Raspberry Pi (A+, B+, Pi 2 model B, Pi 3 model B), and you can increase the throughput to at least 300+ Mbps [...] The Raspberry Pi 3 model B+ includes a Gigabit wired LAN adaptor onboard—though it's still hampered by the USB 2.0 bus speed (so in real world use you get ~224 Mbps instead of ~950 Mbps). [...] The Raspberry Pi 4 model B finally has true Gigabit wired LAN, owing to it's new I/O architecture [...] the Pi 4 can sustain over 900 Mbps"

## Instructions

Install Arch Linux on ARM for Raspberry Pis using [these instructions](https://archlinuxarm.org/platforms/armv7/broadcom/raspberry-pi-2).

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
