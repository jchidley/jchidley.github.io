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

install the required packages
````bash
sudo pacman -S nftables dhcp bind usbutils 
````

Work out what the name of the additional ethernet device is.  I am using an USB3 one.
````bash
lsusb # find out what USB ethernet device is, can do before and after plus diff 
dmesg | grep ax88179 # ax88179 is from above, check to see if driver loaded 
ip addr # see if it's up and has an ip addr and the interface names 
````

set up [/etc/nftables.conf](https://wiki.archlinux.org/index.php/nftables)

```bash
table ip nat_table { 
    chain prerouting { 
        type nat hook prerouting priority filter; policy accept; 
    } 
    
    chain input { 
        type nat hook input priority filter; policy accept; 
    } 

    chain output { 
        type nat hook output priority filter; policy accept; 
    } 
    
    chain postrouting { 
        type nat hook postrouting priority filter; policy accept; 
        oifname "eth1" masquerade 
    } 
} 

table inet routing_table { 
    chain input { 
        type filter hook input priority filter; policy accept; 
        iifname "lo" ip saddr 127.0.0.0/8 ip daddr 127.0.0.0/8 accept 
        ip protocol icmp counter packets 11208 bytes 1671957 accept 
        ct state established accept 
        udp dport 33434-33523 counter packets 0 bytes 0 reject 
        iifname "eth0" tcp dport 53 accept 
        iifname "eth0" udp dport 53 accept 
        iifname "eth0" tcp dport 22 accept 
        iifname "eth0" udp dport 67-68 accept 
        iifname "eth0" tcp dport 591 counter packets 0 bytes 0 accept 
        iifname "eth0" tcp dport 8443 counter packets 0 bytes 0 accept 
        iifname "eth0" tcp dport 8843 counter packets 0 bytes 0 accept 
        iifname "eth0" udp dport 3478 counter packets 0 bytes 0 accept 
        counter packets 42441 bytes 7119203 drop 
    } 

    chain forward { 
        type filter hook forward priority filter; policy accept; 
        ct state established,related accept 
        iifname "eth0" oifname "eth1" accept 
        counter packets 0 bytes 0 drop 
    } 

    chain output { 
        type filter hook output priority filter; policy accept; 
    } 
} 
```


## Links
* [BigDinosaur Blog on Running BIND9 and ISC-DHCP](https://blog.bigdinosaur.org/running-bind9-and-isc-dhcp/)
* [The Ars guide to building a Linux router from scratch](https://arstechnica.com/gadgets/2016/04/the-ars-guide-to-building-a-linux-router-from-scratch/)
*  [Why nftables?](https://wiki.nftables.org/wiki-nftables/index.php/Why_nftables%3F)
*  [Arch Linux nftables](https://wiki.archlinux.org/index.php/nftables)
*  [Getting Gigabit Networking on a Raspberry Pi 2, 3 and B+](https://www.jeffgeerling.com/blogs/jeff-geerling/getting-gigabit-networking)
*  [Pi4 Firmware solves overheating driven throtteling](https://www.jeffgeerling.com/blog/2019/raspberry-pi-4-might-not-need-fan-anymore)
