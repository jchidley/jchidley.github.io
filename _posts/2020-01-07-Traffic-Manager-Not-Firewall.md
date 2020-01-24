---
date: "2020-01-07"
title: "Traffic Manager Not Firewall"
---

# Traffic Manager Not Firewall
That thing called a "Firewall" really is just a traffic manager: security must be done at the device.

## Introduction
I have had the privilege to work with large "blue chip" organisations and some astonishingly able IT people over my career.  One lesson was about the supposed security of private networks vs the Internet.  As one CSO (Chief Security Officer) described it to me "people imagine that their private networks provides a hard shell protecting them when it's actually a sieve".

DMZ, Firewall, etc are all words used to describe the points of contact between private, home or company, networks with the Internet.  They imply that these firewalls and related devices provide strong protection from the Internet whereas nothing could be further from the truth.  Firewalls provide traffic management, keeping inside traffic apart from outside, and this traffic management can certainly help with secuirty.  The less prying eyes on the network the better.  But the idea that the Internet's problems are "out there" is wrong.  Undoubtably there are some devices that have been on other networks, and there are probably other people's devices (guests) that appear on the private network.  All of these devices have thus been exposed to the Internet, and have been exposed to potentially compromised devices in those networks.  Thus, there are devices right now that have effectively imported the Internet's problems into the private network.

So a private network isn't any safer than the Internet.  It is exactly as safe as the Internet.  Assume that your devices are exposed at all times people who are actively trying to break into them.  Any smart device in a private network could be compromised and attack any and all other devices: that smart washing machine, or that printer, for example.  A private network isn't secure but each device in it can be made more secure - and protected from other devices - through good practices on those devices: strong passwords, securely updated, etc.

## Simple Traffic Manager
I know that I said that it wasn't a firewall but here's a simple traffic manager copied from [Gentoo's firewall example](https://wiki.gentoo.org/wiki/Nftables/Examples).


````
define wan_if = "wan0"
define lan_if = "ethusb0"
table ip filter {
	# allow all packets sent by the router itself
	chain output {
		type filter hook output priority 100; policy accept;
	}

	# allow LAN to router, disallow WAN to router
	chain input {
		type filter hook input priority 0; policy accept;
		iifname $lan_if accept
		iifname $wan_if drop
	}

	# allow packets from LAN to WAN, and WAN to LAN if LAN initiated the connection
	chain forward {
		type filter hook forward priority 0; policy drop;
		iifname $lan_if oifname $wan_if accept
		iifname $wan_if oifname $lan_if ct state related,established accept
	}
}
````

## Links
* [Gentoo Nftables/Examples](https://wiki.gentoo.org/wiki/Nftables/Examples)
* [nftables Wiki - Classic perimetral firewall example](https://wiki.nftables.org/wiki-nftables/index.php/Classic_perimetral_firewall_example)
