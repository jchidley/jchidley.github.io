---
date: "2020-01-05"
title: "Building A Raspberry Pi Home Router"
---

# Building A Raspberry Pi Home Router
**TL;DR** Replacing that crappy commerical home router with something that you can be proud of.  Inspired by [this blog](https://blog.bigdinosaur.org/running-bind9-and-isc-dhcp/) and [Ars blog](https://arstechnica.com/gadgets/2016/04/the-ars-guide-to-building-a-linux-router-from-scratch/).

## Introduction

I've bought and used a number of 'home' routers over the years and they've all worked OK but the WiFi has left a lot to be desired, they're very limited in function and configuration.  I wanted to build myself something that I had complete control over and, as a bonus, would teach me somthing about how to setup a proper linux router.    I stumbled across a blog by Ars Techica blog where they did that.  I wanted a minimal build as this helps with both performance and secuirty and with a low power consumption.  Arch linux seemed like a good choice.

I had orginally wanted to use a Raspberry Pi 3 (the latest available) as they are dirt cheap, low power a very small.  But my local Internet ISP is Vigin media and the Pi wouldn't be able to support a throughput of up to 200MBs over an extra USB wired Ethernet interface.  So I looked for the lowest power, lowest cost all-in-one, silent Intel devices.  I found 2 idential Shuttle boxes cheaply on ebay as I wanted to be able to swap them in an out without problems - nothing is more mission critical for a family these days than an internet connection.  In the end I only setup one with dual wired Ethernet and that has been running without issues ever since.

Recently however the Raspberry Pi foundation has released a Pi 4.  This is a cracking bit of kit - I use a 4GB version as a desktop.  This Pi has up to 400Mb capable USB ports, easily good enough for the 100MB connection that I need.  Now is my chance to revisit the work that I did earlier and clean it up a bit.  Then I will probably install it on a 1 or 2GB version of the Pi 4.  It is trivial to make a copy of the SD card.  So if something terrible happens to my router I can run the internet on another older Pi lying around until a new Pi 4 (or 5!) arrives.

[Getting Gigabit Networking on a Raspberry Pi 2, 3 and B+](https://www.jeffgeerling.com/blogs/jeff-geerling/getting-gigabit-networking).  "You can get Gigabit networking working on any current Raspberry Pi (A+, B+, Pi 2 model B, Pi 3 model B), and you can increase the throughput to at least 300+ Mbps (up from the standard 100 Mbps connection via built-in Ethernet).
Note about model 3 B+: The Raspberry Pi 3 model B+ includes a Gigabit wired LAN adapter onboard—though it's still hampered by the USB 2.0 bus speed (so in real world use you get ~224 Mbps instead of ~950 Mbps). So if you have a 3 B+, there's no need to buy an external USB Gigabit adapter if you want to max out the wired networking speed!
Note about model 4: The Raspberry Pi 4 model B finally has true Gigabit wired LAN, owing to it's new I/O architecture. If you're taxing the CPU and USB device bandwidth on the new USB 3.0 ports, you might not get consistent Gbps-range performance, but in my testing so far, the Pi 4 can sustain over 900 Mbps"

## Instructions

Install Arch Linux on ARM for Raspberry Pis using [these instructions](https://archlinuxarm.org/platforms/armv7/broadcom/raspberry-pi-2).

It is possible to configure a simple router based on the [Arch Linux Router](https://wiki.archlinux.org/index.php/Router) instructions.  But will will be going further and installing the software that runs the internet, including the newer firewall nftables.

install the packages
````bash
sudo pacman -S nftables dhcp bind usbutils 
````

## Known Network Interface Names

We're going to do a little extra work here to give our Ethernet (or other network) interfaces known names.  These saves a lot of time troubleshooting later.

I am using a USB3 Gigabit Ethernet device for the best performance.  Here's how I identify the driver and check that it has been loaded.
````bash
lsusb # find out what USB ethernet device is, can do before and after plus diff 
dmesg | grep AX88179 # ax88179 is from above, check to see if driver loaded 
ip addr # to see current interface names and MAC addresses 
````

Give the [network interfaces a known and consistent-desptite-booting name](https://wiki.archlinux.org/index.php/Systemd-networkd#Renaming_an_interface), using the MAC addresses from above.

/etc/systemd/network/10-ethusb0.link
````
[Match]
MACAddress=12:34:56:78:90:ab

[Link]
Description=USB to Ethernet Adapter
Name=ethusb0
````
The other link file will need to be called ```11-intern0.link``` or something memorable. Each interface will need an associated profile. This one is for the "public" or ISP facing interface.
/etc/netctl/ethusb0-profile
````
Description='Public Interface.'
Interface=ethusb0
Connection=ethernet
IP='dhcp
````

and this one for the home network.  I have chosen ```10.0.0.0``` for my private network and ```/24``` gives me about 250 addresses for devices.  I might change this to ```/16``` later.
/etc/netctl/intern0-profile
````
Description='Private Interface'
Interface=intern0
Connection=ethernet
IP='static'
Address=('10.0.0.1/24')
````

These interfaces are enabled with ```netctl enable intern0-profile``` commands.  A reboot is the quickest way to reset things and an ```ip addr``` should show that both interfaces are up and have assigned addresses.

## Setting up nftables

[/etc/nftables.conf](https://wiki.archlinux.org/index.php/nftables)
```bash
flush ruleset
define wan_if = "ethusb0"
define lan_if = "intern0"
table ip nat_table {
        chain prerouting {
                type nat hook prerouting priority 0; policy accept;
        }

        chain input {
                type nat hook input priority 0; policy accept;
        }

        chain output {
                type nat hook output priority 0; policy accept;
        }

        chain postrouting {
                type nat hook postrouting priority 0; policy accept;
                oifname $wan_if masquerade
        }
}
table inet routing_table {
        chain input {
                type filter hook input priority 0; policy accept;
                iifname "lo" ip saddr 127.0.0.0/8 ip daddr 127.0.0.0/8 accept
                ip protocol icmp counter packets 0 accept
                ct state established accept
                udp dport 33434-33523 counter reject
                iifname $lan_if tcp dport domain accept
                iifname $lan_if udp dport domain accept
                iifname $lan_if tcp dport ssh accept
                iifname $lan_if udp dport 67-68 accept

                # for UniFi, check to see what is used, then prune useless rules
                iifname $lan_if tcp dport http-alt counter accept
                iifname $lan_if tcp dport 8443 counter accept
                iifname $lan_if tcp dport 8843 counter accept
                iifname $lan_if udp dport 3478 counter accept

		# Drop everything else
                counter packets 0 dropenp2s0f2
        }

        chain forward {
                type filter hook forward priority 0; policy accept;
                ct state established,related accept
                iifname $lan_if oifname $wan_if accept
                counter drop
        }

        chain output {
                type filter hook output priority 0; policy accept;
        }
}
```


## Links
* [BigDinosaur Blog on Running BIND9 and ISC-DHCP](https://blog.bigdinosaur.org/running-bind9-and-isc-dhcp/)
* [The Ars guide to building a Linux router from scratch](https://arstechnica.com/gadgets/2016/04/the-ars-guide-to-building-a-linux-router-from-scratch/)
*  [Getting Gigabit Networking on a Raspberry Pi 2, 3 and B+](https://www.jeffgeerling.com/blogs/jeff-geerling/getting-gigabit-networking)
*  [Pi4 Firmware solves overheating driven throtteling](https://www.jeffgeerling.com/blog/2019/raspberry-pi-4-might-not-need-fan-anymore)
*  [Arch Linux Router](https://wiki.archlinux.org/index.php/Router)
*  [Renaming an interface](https://wiki.archlinux.org/index.php/Systemd-networkd#Renaming_an_interface)
*  [Why nftables?](https://wiki.nftables.org/wiki-nftables/index.php/Why_nftables%3F)
*  [Arch Linux nftables](https://wiki.archlinux.org/index.php/nftables)

