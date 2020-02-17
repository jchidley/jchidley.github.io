---
date: "2020-01-08"
title: "DNS Setup For DIY Home Router"
---

<!-- markdownlint-disable MD025 -->
# DNS Setup For DIY Home Router
<!-- markdownlint-enable MD025 -->

Modifying my DIY router to support my own DNS.  Now I can build the [Upside-Down-Ternet](http://www.ex-parrot.com/~pete/upside-down-ternet.html)

## Introduction

[Previously](2020-01-05-Building-A-Raspberry-Pi-Home-Router) I built my own DIY router on a Raspberry Pi. Now I am building my own DNS server using [BigDinosaur's notes.](https://blog.bigdinosaur.org/running-bind9-and-isc-dhcp/) and the [Arch Linux specific bind instructions](https://wiki.archlinux.org/index.php/BIND). The aims are to implement DNS for my own domain and link DHCP to DNS.

## Installation

For installation and configuration I just followed Arch Linux's instructions modified by BigDinosuar's article.


```bash
pacman -S wget bind #wget for the root.hint update
```

Executing `/usr/sbin/rndc-confgen -a` generates the `/etc/rndc.key` that is needed for secure updating of DHCP/DNS.  There are references to this key in both the DHCP and DNS configuration files.

```bash
chown named:named /etc/rndc.key
```

This is the revised `/etc/dhcpd.conf` file, fuller explanations are in [BigDinosaur's notes.](https://blog.bigdinosaur.org/running-bind9-and-isc-dhcp/):

```bash
ddns-updates on;
ddns-update-style interim;
ddns-domainname "chidley.test.";
ddns-rev-domainname "in-addr.arpa.";

update-static-leases on;
authoritative;
include "/etc/rndc.key";
allow unknown-clients;

option domain-name "chidley.test";
option domain-name-servers 10.1.0.1, 8.8.8.8;
option subnet-mask 255.255.0.0;
option routers 10.1.0.1;

zone chidley.test. {
    primary localhost; 
    key rndc-key; 
    }

zone 1.10.in-addr.arpa. {
    primary localhost;
    key rndc-key; 
    }

subnet 10.1.0.0 netmask 255.255.0.0 {
  range 10.1.1.1 10.1.200.250;
}

# No DHCP service in DMZ network (192.168.2.0/24)
subnet 192.168.2.0 netmask 255.255.255.0 {
}
```

The `/etc/named.conf` is modified in the light of [the ISC recommendations](https://kb.isc.org/docs/aa-00269):

```bash
acl "trusted" {
	10.1.0.0/16;
	localhost;
	localnets;
	};

include "/etc/rndc.key";

options {
	directory "/var/named";
	pid-file "/run/named/named.pid";
	
	listen-on { any; };
	forwarders { 10.1.0.1; 8.8.8.8; };

	allow-query { any; };
	allow-recursion { trusted; };
	allow-query-cache { trusted; };
	allow-transfer { trusted; };

	version none;
	hostname none;
	server-id none;
};

zone "chidley.test" {
	type master;
	file "chidley.test.zone";
	allow-update { key rndc-key; };
};

zone "1.10.in-addr.arpa" {
	type master;
	file "1.10.rev";
	allow-update { key rndc-key; };
};

zone "." IN {
	type hint;
	file "root.hint";
};
```

`/var/named/chidley.test.zone` based on [Arch Linux example zone file](https://wiki.archlinux.org/index.php/BIND#Creating_a_zonefile):

```bash
$TTL 300	; 5 mins for testing
; chidley.test
@	IN	SOA	alampi.chidley.test. postmaster.chidley.test. (
			1	; Serial
			28800	; Refresh
			1800	; Retry
			604800	; Expire - 1 week
			38400	; minimum (10 hours 40 minutes)
			)
		IN	NS	alarmpi
alarmpi		IN	A	0.0.0.0
localhost	IN	A	127.0.0.1
```

An almost identical one for `/var/named/1.10.rev`:

```bash
$ORIGIN .
$TTL 300	; 5 mins for testing
; 1.10.rev
1.10.in-addr.arpa	IN SOA	alarmpi.chidley.test. webmaster.chidley.test. (
			1	; serial
			10800	; refresh (3 hours)
			3600	; retry (1 hour)
			604800	; expire (1 week)
			38400	; minimum (10 hours 40 minutes)
        	        )
		NS	alarmpi.chidley.test.
```

`chown named:named /var/named/*`

I created [`roothintupdate.sh`](https://wiki.archlinux.org/index.php/Talk:BIND) helper file for updating root.hint

```bash
#!/bin/bash

DATE=`date -u +%Y%m%d`
mv /var/named/root.hint /var/named/root.hint-${DATE}

wget https://www.internic.net/domain/named.root -O /var/named/root.hint
chown named:named /var/named/root.hint
chmod 644 /var/named/root.hint
systemctl restart named
```

For testing: 

```bash
journalctl -f #to view the log as you request DHCP addresses
named-checkzone 1.10.in-addr.arpa 1.10.rev
named-checkzone chidley.test. chidley.test.zone
named-checkconf /etc/named.conf
systemctl status dhcpd4@ethusb0
systemctl status named
```

## Links

* [Upside-Down-Ternet](http://www.ex-parrot.com/~pete/upside-down-ternet.html)
* [Arch linux bind](https://wiki.archlinux.org/index.php/BIND)
* [Talk:BIND](https://wiki.archlinux.org/index.php/Talk:BIND)
* [investigate issues with nsupdate](https://www.semicomplete.com/articles/dynamic-dns-with-dhcp/)
* [BIND from Arch Linux Wiki](https://wiki.archlinux.org/index.php/BIND)

<!-- markdownlint-disable MD034 -->

<!-- markdownlint-enable MD034 -->
