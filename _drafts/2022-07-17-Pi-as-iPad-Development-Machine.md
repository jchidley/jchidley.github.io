---
---

<!-- markdownlint-disable MD025 -->
# Pi as iPad Development Machine
<!-- markdownlint-enable MD025 -->

## Introduction

A sentance

## Build

Disk image
```bash
sudo mount /dev/sda1 /mnt/sda1
sudo dd if=/mnt/sda1/2022-04-04-raspios-bullseye-armhf-lite.img of=/dev/sdb status=progress bs=8M
sudo mount /dev/sdb1 /mnt/sdb1
sudo mount /dev/sdb2 /mnt/sdb2
```

ssh
```bash
sudo touch /mnt/sdb1/ssh
```

WiFi
"Wi-Fi is currently blocked by rfkill.
Use raspi-config to set the country before use."

`sudo raspi-config nonint do_wifi_country GB`

[rfkill soft blocked - Raspberry Pi Forums](https://forums.raspberrypi.com/viewtopic.php?t=319804)

files in /var/lib/systemd/rfkill have a single entry for 0 or 1
on this system:
```bash
platform-3f300000.mmcnr:wlan
platform-fe300000.mmcnr:wlan
platform-soc:bluetooth
```

This is what exists prior to first boot. Contents of both are 1
```bash
platform-3f300000.mmcnr:wlan  platform-fe300000.mmcnr:wlan
```

one of these is set to 1 at some point, possibly on first boot.

enable all interfaces
```bash
echo 0 | sudo tee /var/lib/systemd/rfkill/*
```

unblock spefici interface on pi 4
```bash
echo 0 | sudo tee /var/lib/systemd/rfkill/platform-fe300000.mmcnr\:wlan
```

```bash
sudo tee /mnt/sdb2/etc/wpa_supplicant/wpa_supplicant.conf > /dev/null << "EOF"
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=GB

network={
        ssid="Jack-iPhone"
        psk=d9e0b093b4fcd484e696ec228c4690ee440776ab1c6159502c3059867d730678
}
network={
        ssid="C1"
        psk=896f3ea944b25e1d0e0ec2cc7062f34617d0401b0f2fa670a3840f123d53390d
}
network={
        ssid="C2"
        psk=d8e5cf6b27cb04f5c49d9ed76ab0e2ec396d426dd255de38a323e06a119fb4d5
}
network={
        ssid="C_J"
        psk=28c3058bdeb96e91ba39dc0da4d9ff56bb2e92215a8c194e5cfff99501374583
}
network={
        ssid="MicroPython-AP"
        psk=1e2f01adb61b584f45cb536a056f1b342aab4b9c68188db4fe395995b739e30a
}
network={
        ssid="BT-MNAC3H"
        psk=042e3b47d60f94a45975dab132595ebe44bfca60fa61cb1ff5df3705e40000c7
}
network={
        ssid="CDNMSTUDENTWIFI"
        psk=4c0b9ba1ef7a611be087334df646fcf99edc1953b0c3a6398034545c6f623376
}
EOF
```

USB network
```bash
sudo tee -a /mnt/sdb1/config.txt > /dev/null << "EOF"
dtoverlay=dwc2,dr_mode=peripheral
EOF
sudo sed -i -E -e 's/(^.* )(rootwait.*$)/\1modules-load=dwc2,g_ether \2/' \
    /mnt/sdb1/cmdline.txt
```

Serial console
```bash
sudo tee -a /mnt/sdb1/config.txt > /dev/null << "EOF"
enable_uart=1
EOF
```

First user
[An update to Raspberry Pi OS Bullseye - Raspberry Pi](https://www.raspberrypi.com/news/raspberry-pi-bullseye-update-april-2022/)
```bash
PASS=$(echo 'mypassword' | openssl passwd -6 -stdin)
USERNAME=jack
echo "$USERNAME:$PASS" | sudo tee /mnt/sdb1/userconf.txt 
```

end
```bash
sync
sudo umount /dev/sdb1 /dev/sdb2
```

## Alpine Linux - Chroot

see [downloads | Alpine Linux](https://alpinelinux.org/downloads/)

```bash
cd ~
ALPINEDOWNLOAD='https://dl-cdn.alpinelinux.org/alpine/v3.16/releases/armv7/alpine-minirootfs-3.16.1-armv7.tar.gz'
DOWNLOADEDALPINE="$(echo $ALPINEDOWNLOAD | awk -F/ '{print $NF}')"
wget $ALPINEDOWNLOAD
mkdir ~/alpineRoot
tar -xvf $DOWNLOADEDALPINE -C alpineRoot/
cp /etc/resolv.conf ~/alpineRoot/etc/
cd ~/alpineRoot/
chroot . /bin/ash
sudo chroot . /bin/ash
```

Alpine Linux Chroot
[Alpine Linux in a chroot - Alpine Linux](  https://wiki.alpinelinux.org/wiki/Alpine_Linux_in_a_chroot)
[GitHub - alpinelinux/alpine-chroot-install: Install Alpine Linux in chroot with a breeze. Build ARM on Travis CI or any other x86_64 CI.](https://github.com/alpinelinux/alpine-chroot-install)
[W4TCHGUARD - How to make a portable Alpine linux chroot](https://w4tchguard.neocities.org/20200622-alpine-linux-chroot.html)

General Chroot
[How to Use the chroot Command on Linux](https://www.howtogeek.com/441534/how-to-use-the-chroot-command-on-linux/)
[7.1. Introduction](https://www.linuxfromscratch.org/lfs/view/stable/chapter07/introduction.html)
[chroot - ArchWiki](https://wiki.archlinux.org/title/Chroot#Using_chroot)

Might need virtual, psuedo and temporary filesystems too
[linux - mount dev, proc, sys in a chroot environment? - Super User](https://superuser.com/questions/165116/mount-dev-proc-sys-in-a-chroot-environment)
[6.2. Mounting Virtual Kernel File Systems](https://tldp.org/LDP/lfs/LFS-BOOK-6.1.1-HTML/chapter06/kernfs.html)

## USB Gadget and RaspAP (full setup of an access point)

[Raspberry Pi iPad Pro Setup Simplified - YouTube](https://youtu.be/3UPaI4Hp66Y)
[Raspberry Pi iPad Pro Setup Simplified](https://techcraft.co/videos/2022/5/raspberry-pi-ipad-pro-setup-simplified/)
[Pi4 USB-C Gadget – Ben’s Place](https://www.hardill.me.uk/wordpress/2019/11/02/pi4-usb-c-gadget/)
[Raspberry Pi 4 USB Gadget · GitHub](https://gist.github.com/ianfinch/08288379b3575f360b64dee62a9f453f)
[RaspAP — Simple wireless router setup for Debian-based devices](https://raspap.com)
[Connect your Raspberry Pi 4 to an iPad Pro - Raspberry Pi](https://www.raspberrypi.com/news/connect-your-raspberry-pi-4-to-an-ipad-pro/)

## Pi WiFi Setup 

Need to think about this one. It's like a router setup but not quite.

usb0 as the DNS/DHCP/client interface?
wlan0 as the WAN, or as a LAN? Is both possible or desireable?
Do we need DHCP at all if it's a single machine being worked on?
Routing?
Probably want nftables
do we want to bring up usb0 as the client interface and, if that's not availabe, wlan0 as an AP (access point)?

Or wlan0 as Access Point but manual switching to `wpa_supplicant`?

```code
sudo apt install -y dnsmasq
sudo apt install -y unbound
sudo apt install -y nftables
sudo apt install -y hostapd
```

[Access point as WiFi router/repeater](https://raspberrypi.stackexchange.com/questions/89803/access-point-as-wifi-router-repeater-optional-with-bridge/89804#89804)
[Raspberry Pi Wireless Access Point](https://pimylifeup.com/raspberry-pi-wireless-access-point/comment-page-1/)
[Setting up a Raspberry Pi as a WiFi access point](https://learn.adafruit.com/setting-up-a-raspberry-pi-as-a-wifi-access-point/install-software)
[Setting up a Raspberry Pi 3 as an Access Point](https://learn.sparkfun.com/tutorials/setting-up-a-raspberry-pi-3-as-an-access-point/all)
[Create wireless access point](https://raspberrypi-guide.github.io/networking/create-wireless-access-point)

[pi 3 - Switching between AP and Client mode - Raspberry Pi Stack Exchange](https://raspberrypi.stackexchange.com/questions/62062/switching-between-ap-and-client-mode?noredirect=1&lq=1)
[wifi - Switch between AP and client mode - Raspberry Pi Stack Exchange](https://raspberrypi.stackexchange.com/questions/44184/switch-between-ap-and-client-mode)

[How to scan for IP addresses on your network with Linux | TechRepublic](https://www.techrepublic.com/article/how-to-scan-for-ip-addresses-on-your-network-with-linux/)

## Code-Server

[VSCode on iPad Pro - Full Setup Guide with Raspberry Pi](https://techcraft.co/videos/2022/2/vscode-on-ipad-pro-full-setup-guide-with-raspberry-pi/)
[code-server - debian dependencies](https://coder.com/docs/code-server/latest/npm#nodejs-version)

```bash
sudo apt-get install -y \
  build-essential \
  pkg-config \
  python3
```

On a Raspberry Pi install the latest version of nodejs [Install Node js and Npm latest Version on Raspberry Pi 4?](https://officialrajdeepsingh.dev/install-node-js-and-npm-latest-version-on-raspberry-pi-4/)

`uname -m` to check the particular version required and then download it from [Download | Node.js](https://nodejs.org/en/download/) using `wget`, then extract and move it to the correct place. For example:

```bash
wget https://nodejs.org/dist/v16.16.0/node-v16.16.0-linux-armv7l.tar.xz
tar xvf node-v16.16.0-linux-armv7l.tar.xz node-v16.16.0-linux-armv7l/
cd node-v16.16.0-linux-armv7l/
sudo cp -R * /usr/local/
node -v
```

```bash
npm config set python python3
sudo npm install --global yarn
```

```bash
yarn global add code-server
# Or: npm install -g code-server
code-server
# Now visit http://127.0.0.1:8080. Your password is in ~/.config/code-server/config.yaml
```

```bash
# access from any node on network
sed -E -i 's/(^\s*)(bind-addr:\s)(.*$)/\20.0.0.0:8080/g' ~/.config/code-server/config.yaml
# temporaily remove password
sed -E -i 's/(^\s*)(auth:\s)(.*$)/\2none/g' ~/.config/code-server/config.yaml
```

Go to the site (e.g. http://pilite.local:8080) and then add it to the home screen of the iPad using the share key. This adds a nice icon to the desktop

```bash
#add password back
sed -E -i 's/(^\s*)(auth:\s)(.*$)/\2password/g' ~/.config/code-server/config.yaml
```

```bash
sudo tee /etc/systemd/system/code-server.service > /dev/null << "EOF"
[Unit]
Description=code-server
After=network.target

[Service]
User=jack
Group=jack

WorkingDirectory=/home/jack
Environment="PATH=/usr/local/bin"
ExecStart=/home/jack/.yarn/bin/code-server

[Install]
WantedBy=multi-user.target
EOF
```

[sed Appending a line to a file only if it does not already exist, removing comment if that exists - Stack Overflow](https://stackoverflow.com/a/49852337/3617057)

```bash
sed -i \
    -E -e '/^#*\s*(cert:).*$/{s//\1 true/;:a;n;ba;q}' \
    -e '$acert: true' ~/.config/code-server/config.yaml
sed -i \
    -E -e '/^#*\s*(cert-host:).*$/{s//\1 pilite.local/;:a;n;ba;q}' \
    -e '$acert-host: pilite.local' ~/.config/code-server/config.yaml
```

[Visual Studio Code Server](https://code.visualstudio.com/docs/remote/vscode-server)

## Links

<!-- markdownlint-disable MD034 -->
<!-- markdownlint-enable MD034 -->

* [VSCode on iPad Pro - Full Setup Guide with Raspberry Pi](https://techcraft.co/videos/2022/2/vscode-on-ipad-pro-full-setup-guide-with-raspberry-pi/)
