---
date: "2020-02-09"
title: "Alpine Linux Install"
---
<!-- 2020-02-09-Alpine-Linux-Install.md -->

<!-- markdownlint-disable MD025 -->
# Alpine Linux Install
<!-- markdownlint-enable MD025 -->

## Introduction

## Install

boot USB (or other prepared) boot device and run the setup program

```bash
setup-alpine
```

I manually configured the partitions because I'm running and EFI system.

## EFI boot

create `.nsh` file like this:

```bash
fs0:
cd /alpine1shuttle1
vmlinux ... root... modules... initrd=/alpine1shuttle1/initramfs-lts
```

the boot line is modified from the extlinux.cfg file.  Note the initrd comes at the end and includes the full path on the EFI system drive.

## xfce4 desktop

```bash
setup-xorg-base xfce4 xfce4-terminal lightdm-gtk-greeter xfce-polkit xfce4-screensaver consolekit2 dbus-x11 sudo
vi /etc/apk/repositories
```

<!-- markdownlint-disable MD034 -->
uncomment http://dl-cdn.alpinelinux.org/alpine/edge/community or similar
<!-- markdownlint-enable MD034 -->

```bash
apk update
apk add xf86-video-intel # already added
apk add xf86-input-mouse xf86-input-keyboard
setxkbmap gb
adduser -g 'Jack' jack
addgroup jack wheel
visudo
lbu include /home
rc-service dbus start # temp
rc-service lightdm start # temp
rc-update add dbus # rebooted
rc-update add lightdm # rebooted
```

## Firefox

```bash
apk add firefox-esr
```

## The End

This is enough to get a normal desktop in under 2G of disk space.

## Links

* [XFCE Setup](https://wiki.alpinelinux.org/wiki/XFCE_Setup)
* [Enable Community Repository](https://wiki.alpinelinux.org/wiki/Enable_Community_Repository)
<!-- markdownlint-disable MD034 -->
https://serverfault.com/a/821235
<!-- markdownlint-enable MD034 -->
