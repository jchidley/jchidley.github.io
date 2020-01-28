---
date: "2020-01-27"
title: "Simplest possible Linux boot"
---
<!-- 2020-01-27-Simplest-possible-Linux-boot -->

<!-- markdownlint-disable MD025 -->
# Simplest possible Linux boot
<!-- markdownlint-enable MD025 -->

## Introduction

need to install suitable packages on the starter system

```bash
pacman -S musl cpio base_devel
```

[if something's missing, like bc](https://github.com/landley/mkroot/issues/2)

```bash
rm -rf airlock
./cross.sh x86_64 ./mkroot.sh HOST_EXTRA='bc'
```

## Links

* [mkroot - simple linux system builder, bootable under qemu for multiple architectures.](https://github.com/landley/mkroot)
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

<!-- markdownlint-disable MD034 -->
* (https://en.wikipedia.org/wiki/Linux_startup_process)
* (https://en.wikipedia.org/wiki/Initial_ramdisk)
* (https://wiki.archlinux.org/index.php/Arch_boot_process)
* (https://wiki.archlinux.org/index.php/EFISTUB)
* (https://wiki.archlinux.org/index.php/Microcode#EFISTUB)
* (https://glowingthumb.com/uefi-shell-scripts-3-of-3/)
<!-- markdownlint-enable MD034 -->
