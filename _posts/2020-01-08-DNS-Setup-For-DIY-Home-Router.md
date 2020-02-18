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

## Private Domains

There are 2 sets of top level domains (tlds) that can be used in private networks:

* [The IETF](https://www.ietf.org/) [reserved](https://tools.ietf.org/html/rfc2606) `.test .example .invalid .localhost`
* [ICAN](https://www.icann.org/) [will never allocate](https://features.icann.org/addressing-new-gtld-program-applications-corp-home-and-mail) `.corp .home .mail`

I am using chidley.test as the domain name here.

## Installation

For installation and configuration I just followed Arch Linux's instructions modified by BigDinosuar's article.

```bash
pacman -S wget bind #wget for the root.hint update
```

Executing `/usr/sbin/rndc-confgen -a` generates the `/etc/rndc.key` that is needed for secure updating of DHCP/DNS.  `named` needs to be able to read the key file.

```bash
chown named:named /etc/rndc.key
```

Here is the `/etc/dhcpd.conf` file that has been adjusted from the [most basic one](https://wiki.archlinux.org/index.php/Dhcpd) for dynamic updates of DNS.  See [BigDinosaur's](https://blog.bigdinosaur.org/running-bind9-and-isc-dhcp/) and [semicomplete's](https://www.semicomplete.com/articles/dynamic-dns-with-dhcp/) notes for more explanations.

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
The Arch Linx Wiki has [concise information on BIND](https://wiki.archlinux.org/index.php/BIND) with the simplest of examples, this has been extended follwing [the ISC recommendations](https://kb.isc.org/docs/aa-00269).  I used BigDinosaur and semicomplete to adjust it for dynamic updates of DHCP and DNS

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

`/var/named/chidley.test.zone` is based on [Arch Linux example zone file](https://wiki.archlinux.org/index.php/BIND#Creating_a_zonefile):

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

BIND (named) needs read and write access to all of the files in `/var/named`: `chown named:named /var/named/*`

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

## Testing, testing, testing

These configuration files are very hard to get right, so testing is essential.  Here are some commands that I used for this:

```bash
journalctl -f #to view the log as you request DHCP addresses
named-checkzone 1.10.in-addr.arpa 1.10.rev
named-checkzone chidley.test. chidley.test.zone
named-checkconf /etc/named.conf
systemctl status dhcpd4@ethusb0
systemctl status named
```

```bash
% nsupdate
> server 10.1.0.1
> key rndc-key N8Hk2RUFO84bEVl3uGTD2A==
> zone test
> update add 20.20.1.10.in-addr.arpa 600 IN PTR deleteme.chidley.test.
> send
> update add deleteme.chidley.test. 600 IN A 10.1.20.20
> send
```

## Links

* [Upside-Down-Ternet](http://www.ex-parrot.com/~pete/upside-down-ternet.html)
* [BigDinosaur's notes](https://blog.bigdinosaur.org/running-bind9-and-isc-dhcp/)
* [The IETF](https://www.ietf.org/) 
* [test example invalid and localhost reserved tlds](https://tools.ietf.org/html/rfc2606) `.test .example .invalid .localhost`
* [ICAN](https://www.icann.org/) 
* [Non allocation of corp home and mail tlds](https://features.icann.org/addressing-new-gtld-program-applications-corp-home-and-mail)
* [Arch Linux DHCPD instructions](https://wiki.archlinux.org/index.php/Dhcpd)
* [semicomplete's notes on dynamic update of DNS via DHCP](https://www.semicomplete.com/articles/dynamic-dns-with-dhcp/)
* [Arch linux bind](https://wiki.archlinux.org/index.php/BIND)
* [Talk:BIND](https://wiki.archlinux.org/index.php/Talk:BIND)
* [Arch Linux example zone file](https://wiki.archlinux.org/index.php/BIND#Creating_a_zonefile)
* [ISC recommendations for trust](https://kb.isc.org/docs/aa-00269)

<!-- markdownlint-disable MD034 -->

<!-- markdownlint-enable MD034 -->
