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

I have had the privilege to work with large "blue chip" organisations and some astonishingly able IT people over my career.  One lesson was about the supposed security of private networks vs the Internet.  As one CSO (Chief Security Officer) said "People imagine that their networks provide a hard protective shell.  That shell is riddled with holes and their private networks contain suspect devices".

DMZ, Firewall, etc are all words used to describe the points of contact between private, home or company, networks with the Internet.  They imply that these firewalls and related devices provide strong protection from the Internet whereas nothing could be further from the truth.  Firewalls provide traffic management, keeping inside traffic apart from outside, and this traffic management can certainly help with security.  The less prying eyes on the network the better.  

The idea that security problems are "out there" on the Internet and other networks is wrong. Even in the best organisations, with well managed networks, there will be suspect device: devices that have been on other networks, guest devices, compromised devices and devices that cannot be made secure (old pinters, for example). Thus any network may contain devices that can attack other devices from within the "secure" network. It is possible, but not trivial, to secure networks but don't imagine that a "firewall" suddenly makes your network secure.

So a private network isn't any safer than the Internet. It is exactly as safe as the Internet. Assume that your devices are exposed at all times people who are actively trying to break into them. Any smart device in a private network could be compromised and attack any and all other devices: that smart washing machine, or that printer, for example. A private network isn't secure but each device in it can be made more secure - and protected from other devices - through good practices on those devices: strong passwords, securely updated, etc.

## Simple Traffic Manager

This simple traffic manager allows all internal traffic to access and pass through the router but will only allow traffic in the reverse direction if it has been started from a device in the internal network.  It will drop all traffic from [Martian](https://en.wikipedia.org/wiki/Martian_packet) IP addresses.

```bash
cat > /etc/nftables.conf << "EOF"
#!/usr/sbin/nft -f
flush ruleset

define wan = eth0
define lan = eth1
define private_special_purpose = {10.0.0.0/8, 100.64.0.0/10, 172.16.0.0/12, 192.0.0.0/24, 192.168.0.0/16, 198.18.0.0/15}
define documentation_special_purpose = {192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24}
define internet_special_purpose = {192.88.99.0/24, 224.0.0.0/4, 240.0.0.0/4}

# Martian packets "contain a source or destination address that is reserved for special-use" https://en.wikipedia.org/wiki/Martian_packet
define martians = {$private_special_purpose, $documentation_special_purpose, $internet_special_purpose}

# Add the "log counter" options to monitor policies 
table ip filter {
  chain input {
    type filter hook input priority filter; policy drop;

    meta if $wan ip saddr $martians drop

    ct state invalid drop

    meta if lo ct state new accept

    meta if $lan ct state new accept

    icmp type echo-request accept

    ct state established,related accept
  }

  chain forward {
    type filter hook forward priority filter; policy drop;

    meta if $lan meta oif $wan accept

    meta if $wan meta oif $lan ct state established,related accept
  }

# Output hook is accept by default 

}

# first packets in a specific communiction touch the nat table 
# - the rest are then established, connected
table ip nat {
  chain postrouting {
    type nat hook postrouting priority srcnat;

    oif $wan masquerade persistent
  }
}
EOF
```

Followed by:

```bash
nft -f /etc/nftables.conf
nft list ruleset # view result
```

### Using IPTABLES Examples

If you have an set of `iptables` rules that you would like to use in `nft` you can use the following commands to see what the ruleset looks like in `nftables`:

Use the commands 
```
iptables-save > save.txt
iptables-restore-translate -f save.txt
```

## Links

* [Moving from iptables to nftables](https://wiki.nftables.org/wiki-nftables/index.php/Moving_from_iptables_to_nftables)
* [Reserved IP addresses](https://en.wikipedia.org/wiki/Reserved_IP_addresses)
* [nftables wiki](https://wiki.nftables.org/wiki-nftables/index.php/Main_Page)
* [Quick reference-nftables in 10 minutes](https://wiki.nftables.org/wiki-nftables/index.php/Quick_reference-nftables_in_10_minutes)
* [Alpine Linux Stateful Firewall - deadnull](https://ronvalente.net/posts/alpine-firewall/)