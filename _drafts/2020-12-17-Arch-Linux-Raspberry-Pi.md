---
date: "2020-12-17"
title: "Arch Linux Raspberry Pi"
---

<!-- markdownlint-disable MD025 -->
# Arch Linux Raspberry Pi
<!-- markdownlint-enable MD025 -->


Copy /etc/fstab from Raspbian OS 64 install and change PARTUUID to those shown 
lsblk -o PARTUUID,NAME

[Mirrors - ArchWiki](https://wiki.archlinux.org/index.php/mirrors)
Change the mirror to eu ones early

## x windows

pacman -S xorg xinit # possibly xorg-server too
pacman -S xf86-video-fbdev # need to check with Raspbian OS 64 

[VC4 and V3D OpenGL drivers for Raspberry Pi: an update - Raspberry Pi](https://www.raspberrypi.org/blog/vc4-and-v3d-opengl-drivers-for-raspberry-pi-an-update/)

[dwm - dynamic window manager | suckless.org software that sucks less](https://dwm.suckless.org)
[st - simple terminal | suckless.org software that sucks less](https://st.suckless.org)- no terminal otherwise
[dmenu](https://tools.suckless.org/dmenu/)

## ntp

[Network Time Protocol daemon - ArchWiki](https://wiki.archlinux.org/index.php/Network_Time_Protocol_daemon#Running_in_a_chroot)

### WiFi

[New Raspberry Pi 400 - ARM - Manjaro Linux Forum](https://forum.manjaro.org/t/new-raspberry-pi-400/35555)


<!-- markdownlint-disable MD034 -->

## Links

* [archlinux - Install Xorg on Arch-Linux-ARM - Raspberry Pi Stack Exchange](https://raspberrypi.stackexchange.com/questions/116446/install-xorg-on-arch-linux-arm#comment200213_116446)
* 

<!-- markdownlint-enable MD034 -->