﻿---
date: "2020-01-08"
title: "DNS Setup For DIY Home Router"
---

# DNS Setup For DIY Home Router
Modifying my DIY router to support my own DNS.  Now I can build the [Upside-Down-Ternet](http://www.ex-parrot.com/~pete/upside-down-ternet.html)

## Introduction

[Previously](2020-01-05-Building-A-Raspberry-Pi-Home-Router) I built my own DIY router on a Raspberry Pi.  Now I am building my own DNS server using [BigDinosaur's notes.](https://blog.bigdinosaur.org/running-bind9-and-isc-dhcp/) and the [Arch Linux specific bind instructions](https://wiki.archlinux.org/index.php/BIND).  The aims are to implement DNS for my own domain and link DHCP to DNS.

## Installation
For installation and configuration I just followed Arch Linux's instructions modified by BigDinosuar's article.
````
pacman -S wget bind #wget for the root.hint update

Executing ```/usr/sbin/rndc-confgen -a``` generates the ```/etc/rndc.key``` that is needed for secure updating of DHCP/DNS.  There are references to this key in both the DHCP and DNS configuration files.

This is the revised ```/etc/dhcpd.conf``` file, fuller explanations are in [BigDinosaur's notes.](https://blog.bigdinosaur.org/running-bind9-and-isc-dhcp/):
````
ddns-updates on;
ddns-update-style interim;
update-static-leases on;
authoritative;
include "/etc/rndc.key";
allow unknown-clients;
use-host-decl-names on;
default-lease-time 1814400;
max-lease-time 1814400;
log-facility local7;

option domain-name-servers 8.8.8.8, 8.8.4.4;
option subnet-mask 255.255.0.0;
option routers 10.1.0.1;
option domain-name-servers 10.1.0.1;
option domain-name "chidley.net";
ddns-domainname "chidley.net.";
ddns-rev-domainname "in-addr.arpa.";

zone chidley.net. {
    primary localhost; 
    key rndc-key; 
    }

zone 1.10.in-addr.arpa. {
    primary localhost;
    key rndc-key; 
    }

subnet 10.1.0.0 netmask 255.255.0.0 {
    range 10.1.100.1 10.1.200.250;
}

# No DHCP here
subnet 10.0.0.0 netmask 255.255.0.0 {
}
````

The ```named.conf``` is modified in the light of [the ISC recommendations](https://kb.isc.org/docs/aa-00269):
````
acl "trusted" {
	10.1.0.0/16;
    localhost;
    localnets;
 };

include "/etc/rndc.key";

options {
    directory "/var/named";
    pid-file "/run/named/named.pid";

    listen-on-v6 { any; };
    listen-on { any; };
    forwarders { 8.8.8.8; 8.8.4.4; };

    allow-query { trusted; };
    allow-recursion { trusted; };
    allow-query-cache { trusted; };
    allow-transfer { trusted; };
    allow-update { none; };

    version none;
    hostname none;
    server-id none;
};

zone "chidley.net" {
    type master;
    file "chidley.net.hosts";
    allow-update { key rndc-key; };
};

zone "1.10.in-addr.arpa" {
    type master;
    file "1.10.rev";
    allow-update { key rndc-key; };
};

zone "localhost" IN {
    type master;
    file "localhost.zone";
};

zone "0.0.127.in-addr.arpa" IN {
    type master;
    file "127.0.0.zone";
};

zone "1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa" {
    type master;
    file "localhost.ip6.zone";
};

zone "." IN {
    type hint;
    file "root.hint";
};
````

```chidley.net.hosts```:
````
$ORIGIN .
$TTL 907200 ; 1 week 3 days 12 hours
; chidley.net.
chidley.net  IN  SOA  alarmpi1.chidley.net. postmaster.chidley.net. (
                                        20200107 ; Serial
                                        28800      ; Refresh
                                        1800       ; Retry
                                        604800     ; Expire - 1 week
                                        86400 )    ; Minimum
NS      alarmpi1.chidley.net.

$ORIGIN chidley.net.
$TTL 3600       ; 1 hour for testing
````

An almost identical one for ```1.10.rev```:
````
$ORIGIN .
$TTL 907200 ; 1 week 3 days 12 hours
; 1.10.in-addr.arpa
1.10.in-addr.arpa  IN  SOA  alarmpi1.chidley.net. postmaster.chidley.net. (
                                        20200107 ; Serial
                                        28800      ; Refresh
                                        1800       ; Retry
                                        604800     ; Expire - 1 week
                                        86400 )    ; Minimum
NS      alarmpi1.chidley.net.

$ORIGIN 1.10.in-addr.arpa
$TTL 3600       ; 1 hour for testing
````


I created [```roothintupdate.sh```](https://wiki.archlinux.org/index.php/Talk:BIND) helper file for updating root.hint
````
#!/bin/bash

DATE=`date -u +%Y%m%d`
mv /var/named/root.hint /var/named/root.hint-${DATE}

wget https://www.internic.net/domain/named.root -O /var/named/root.hint
chown named:named /var/named/root.hint
chmod 644 /var/named/root.hint
systemctl restart named
````


## Links
* [Upside-Down-Ternet](http://www.ex-parrot.com/~pete/upside-down-ternet.html)
* [Arch linux bind](https://wiki.archlinux.org/index.php/BIND)
* [Talk:BIND](https://wiki.archlinux.org/index.php/Talk:BIND)