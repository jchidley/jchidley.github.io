---
date: "2020-01-27"
title: "Simplest possible Linux boot"
---
<!-- 2020-01-27-Simplest-possible-Linux-boot -->

<!-- markdownlint-disable MD025 -->
# Simplest possible Linux boot
<!-- markdownlint-enable MD025 -->

## Introduction

## Get mkroot

```bash
git clone https://github.com/landley/mkroot
less mkroot/README # instructions
```

need to install suitable packages on the starter system

```bash
pacman -S qemu cpio bc # may not need base-devel musl
```

download native compiler from https://mkroot.musl.cc/latest
Extract the native compiler in a suitable directory

```bash
mkdir mcm
cd mcm
wget https://mkroot.musl.cc/latest/x86_64-linux-musl-native.tgz
bsdtar xvf x86_64-linux-musl-native.tgz
ln -s ~/mkroot/mcm ~/mcm
```

Some native and cross compilers:

```bash
https://mkroot.musl.cc/latest/aarch64-linux-musl-cross.tgz

aarch64-linux-musl-cross.tgz
aarch64-linux-musl-native.tgz
aarch64_be-linux-musl-cross.tgz
aarch64_be-linux-musl-native.tgz
arm-linux-musleabi-cross.tgz
arm-linux-musleabi-native.tgz
arm-linux-musleabihf-cross.tgz
arm-linux-musleabihf-native.tgz
armeb-linux-musleabi-cross.tgz
armeb-linux-musleabi-native.tgz
armeb-linux-musleabihf-cross.tgz
armeb-linux-musleabihf-native.tgz
armel-linux-musleabi-cross.tgz
armel-linux-musleabi-native.tgz
armel-linux-musleabihf-cross.tgz
armel-linux-musleabihf-native.tgz
armv5l-linux-musleabihf-cross.tgz
armv5l-linux-musleabihf-native.tgz
armv7l-linux-musleabihf-cross.tgz
armv7l-linux-musleabihf-native.tgz
armv7m-linux-musleabi-cross.tgz
armv7m-linux-musleabi-native.tgz
armv7r-linux-musleabihf-cross.tgz
armv7r-linux-musleabihf-native.tgz 

x86_64-linux-musl-cross.tgz
x86_64-linux-musl-native.tgz
x86_64-linux-muslx32-cross.tgz
x86_64-linux-muslx32-native.tgz
```

[if something's missing, like bc](https://github.com/landley/mkroot/issues/2)

```bash
pacman -S bc
rm -rf airlock
./cross.sh x86_64 ./mkroot.sh HOST_EXTRA='bc'
```

## Links

* [mkroot - simple linux system builder, bootable under qemu for multiple architectures.](https://github.com/landley/mkroot)
* [rob's blog](http://landley.net/notes.html)
* [J-Core Open Processor](https://j-core.org/)
* [Dropbear SSH](https://matt.ucc.asn.au/dropbear/dropbear.html) & [github for it](https://github.com/mkj/dropbear)
* [Bash scripting cheatsheet](https://devhints.io/bash)
* [Aboriginal Linux](https://landley.net/aboriginal/about.html)
* [Blog about successor to Aboriginal Linux](https://landley.net/notes-2016.html#17-05-2016)
* [beginnings of mkroot](http://lists.landley.net/pipermail/mkroot-landley.net/2017-May/000000.html)
* [Institutional memory and reverse smuggling](https://web.archive.org/web/20120111055334/http://wrttn.in/04af1a)
* [Use " and not ' on Qemu on Windows](https://github.com/dhruvvyas90/qemu-rpi-kernel/issues/71)
* [Using QEMU to emulate a Raspberry Pi](https://blog.agchapman.com/using-qemu-to-emulate-a-raspberry-pi/)
* [The Rise and Fall of Copyleft](http://landley.net/talks/ohio-2013.txt)
* [booting a fresh linux kernel on qemu](https://ops.tips/notes/booting-linux-on-qemu/)
* [How to Build A Custom Linux Kernel For Qemu](https://mgalgs.github.io/2015/05/16/how-to-build-a-custom-linux-kernel-for-qemu-2015-edition.html)
* [Fast linux kernel testing with qemu](http://ncmiller.github.io/2016/05/14/linux-and-qemu.html)
* [arch linux BusyBox](https://wiki.archlinux.org/index.php/BusyBox)
* [About Aboriginal Linux](http://landley.net/aboriginal/about.html#selfhost)
* [musl libc](https://www.musl-libc.org/)
* [Hello world for bare metal ARM using QEMU](https://balau82.wordpress.com/2010/02/28/hello-world-for-bare-metal-arm-using-qemu/)
* [Write messages to stdout from anywhere, by modifying pl011_console_putchar](https://github.com/torvalds/linux/blob/master/drivers/tty/serial/amba-pl011.c)
* [j-core mailing list](https://lists.j-core.org/mailman/listinfo/j-core)

<!-- markdownlint-disable MD034 -->
* (https://en.wikipedia.org/wiki/Linux_startup_process)
* (https://en.wikipedia.org/wiki/Initial_ramdisk)
* (https://wiki.archlinux.org/index.php/Arch_boot_process)
* (https://wiki.archlinux.org/index.php/EFISTUB)
* (https://wiki.archlinux.org/index.php/Microcode#EFISTUB)
* (https://glowingthumb.com/uefi-shell-scripts-3-of-3/)
<!-- markdownlint-enable MD034 -->
