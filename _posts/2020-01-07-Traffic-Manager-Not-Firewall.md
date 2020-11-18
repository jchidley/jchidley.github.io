---
date: "2020-01-07"
title: "Traffic Manager Not Firewall"
---
<!-- 2020-01-07-Traffic-Manager-Not-Firewall.md -->

<!-- markdownlint-disable MD025 -->
# Traffic Manager Not Firewall
<!-- markdownlint-enable MD025 -->

That thing called a "Firewall" really is just a traffic manager: every device must be individually secure.

## Introduction

I have had the privilege to work with large "blue chip" organisations and some astonishingly able IT people over my career.  One lesson was about the supposed security of private networks vs the Internet.  As one CSO (Chief Security Officer) said "people imagine that their networks provide a hard protective shell when that shell is riddled with holes and is filled with suspect devices".

DMZ, Firewall, etc are all words used to describe the points of contact between private, home or company, networks with the Internet.  They imply that these firewalls and related devices provide strong protection from the Internet whereas nothing could be further from the truth.  Firewalls provide traffic management, keeping inside traffic apart from outside, and this traffic management can certainly help with secuirty.  The less prying eyes on the network the better.  But the idea that the Internet's problems are "out there" is wrong.  Undoubtably there are some devices that have been on other networks, and there are probably other people's devices (guests) that appear on the private network.  All of these devices have thus been exposed to the Internet, and have been exposed to potentially compromised devices in those networks.  Thus, there are devices right now that have effectively imported the Internet's problems into the private network.

So a private network isn't any safer than the Internet.  It is exactly as safe as the Internet.  Assume that your devices are exposed at all times people who are actively trying to break into them.  Any smart device in a private network could be compromised and attack any and all other devices: that smart washing machine, or that printer, for example.  A private network isn't secure but each device in it can be made more secure - and protected from other devices - through good practices on those devices: strong passwords, securely updated, etc.

## Simple Traffic Manager

This is built on the examples from the [nftables wiki](https://wiki.nftables.org/wiki-nftables/index.php/Main_Page), specifically the [perimitral firewall example](https://wiki.nftables.org/wiki-nftables/index.php/Classic_perimetral_firewall_example).

```bash
cat > /etc/nftables.conf << "EOF"
flush ruleset
define wan_if = "wan0"
define lan_if = "ethusb0"

# From the original ruleset for NATing
# 'ip' is for IPv4 only
table ip nat_table {
        chain postrouting {
                type nat hook postrouting priority 0; policy accept;
                oifname $wan_if masquerade
        }
}

# 'inet' is for both IPv4 and IPv6
table inet filter {
        chain global {
                # accept traffic originated from us
                ct state established,related accept
                ct state invalid drop
                # ping
                ip protocol icmp accept
                ip6 nexthdr icmpv6 accept
                # DNS
                udp dport 53 accept
                tcp dport 53 accept
        }

        chain input {
                type filter hook input priority 0 ; policy drop;
                jump global
                iifname "lo" accept
                # your rules for traffic to the firewall here
}

        chain forward {
                type filter hook forward priority 0;
                jump global
                # Accept LAN to WAN
                iifname $lan_if oifname $wan_if accept
                counter drop
        }
}
EOF
```

Followed by:

```bash
nft -f /etc/nftables.conf
nft list ruleset # view result
```

## Links

* [nftables wiki](https://wiki.nftables.org/wiki-nftables/index.php/Main_Page)
* [nftables Wiki - Classic perimetral firewall example](https://wiki.nftables.org/wiki-nftables/index.php/Classic_perimetral_firewall_example)
* [Quick reference-nftables in 10 minutes](https://wiki.nftables.org/wiki-nftables/index.php/Quick_reference-nftables_in_10_minutes)
* [Recognize Martian Addresses for Routing - TechLibrary - Juniper Networks](https://www.juniper.net/documentation/en_US/junos/topics/topic-map/recognize-martian-addr-routing.html)
* [Alpine Linux Stateful Firewall - deadnull](https://ronvalente.net/posts/alpine-firewall/)