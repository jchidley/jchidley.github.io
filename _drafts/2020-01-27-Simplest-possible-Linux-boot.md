---
date: "2020-01-27"
title: "Simplest possible Linux boot"
---
<!-- 2020-01-27-Simplest-possible-Linux-boot -->

<!-- markdownlint-disable MD025 -->
# Simplest possible Linux boot
<!-- markdownlint-enable MD025 -->

## Introduction

All of this comes from Rob Landley's talk at the Linux Foundation [Tutorial: Building the Simplest Possible Linux System - Rob Landley, se-instruments.com - YouTube](https://www.youtube.com/watch?v=Sk9TatW9ino)

For the simplest system required to build itself, [there are 4 conceptual components required](https://youtu.be/Sk9TatW9ino?t=160):

* Kernel - e.g, Linux
* C library - musl libc
* Toolchain - compiler, linker, etc
* Command-Line utilities - busybox, toybox

* [Aboringinal Linux, and the actual 7 packages required](https://www.youtube.com/watch?v=Sk9TatW9ino&feature=youtu.be&t=225) [GitHub source](https://github.com/landley/aboriginal)
* [Linux print statements, from anywhere at any time](https://youtu.be/Sk9TatW9ino?t=857) Writing to a real serial device (pl011 console putchar) anytime, even during boot, from Linux
* [Cross compiling](https://youtu.be/Sk9TatW9ino?t=1095)
* [Simple main.c hello world as init](https://youtu.be/Sk9TatW9ino?t=1203)
* [Hello World, bare metal](https://youtu.be/Sk9TatW9ino?t=408) [Freedom Embedded: Hello world for bare metal ARM using QEMU](https://balau82.wordpress.com/2010/02/28/hello-world-for-bare-metal-arm-using-qemu/)
* [QEMU Explanation](https://youtu.be/Sk9TatW9ino?t=580)
* [Linux Kernel booting](https://youtu.be/Sk9TatW9ino?t=1461) mounting a root file system, cpio archive extracted into initramfs (ramfs/tmpfs) and looks * for `init` (previously `linuxrc`)
* [Linux File Systems Explanations](https://youtu.be/Sk9TatW9ino?t=1535) Block backed (as used on a disk, like ext2), pipe backed (it’s a program providing data over a protocol like NFS and SAMBA do over a network), RAM backed file system (using a system like the disk cache e.g. ramfs, tmpfs), synthetic file system (proc, sys). `initrd` is a RAM disk is a block backed file system stored in RAM so this also needs a page cache - less efficient than ramfs.
* [running `init` from top level directory](https://youtu.be/Sk9TatW9ino?t=1800)  
* [linux/init/main.c `start_kernel` function](https://www.youtube.com/watch?v=Sk9TatW9ino&feature=youtu.be&t=1840) and [`kernel_init` function](https://github.com/torvalds/linux/blob/master/init/main.c) has a list of backup places to look fir init, including `/bin/sh`.
* [what happens during Kernel booting](https://youtu.be/Sk9TatW9ino?t=1461) Boot, mount Linux root file system, can use CPIO archive that is extracted to, say, initramfs or boot from a block device (root= option), run a program called “init” vmLinux is an ELF format and then some transformatio (binary?) to get bzImage
* [`initrd` kernel parameter](https://youtu.be/Sk9TatW9ino?t=2040) is designed for block devices but will use `cpio` and extract to `initramfs`.  Also * `rdinit` has been used in the past
* [Linux kernel command line](https://youtu.be/Sk9TatW9ino?t=2125) required `console=` serial console
* [www.kernel.org Documentation](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation?h=v5.9.6)
* [The kernel’s command-line parameters](https://www.kernel.org/doc/html/v4.14/admin-guide/kernel-parameters.html)
* [busybox addition to init and configuration of](https://youtu.be/Sk9TatW9ino?t=2400)
* Defconfig is default configuration, `make help` will often tell you the various targets
* [kbuild - What exactly does Linux kernel’s `make defconfig` do? - Stack Overflow](https://stackoverflow.com/questions/41885015/what-exactly-does-linux-kernels-make-defconfig-do)

* [Repackage a cpio as squashfs or ext2](https://youtu.be/Sk9TatW9ino?t=3496) using [mksquashfs](https://manpages.debian.org/jessie/squashfs-tools/mksquashfs.1.en.html) or [mkfs.ext2](https://linux.die.net/man/8/mkfs.ext2) respectively
* [Loop back device](https://youtu.be/Sk9TatW9ino?t=3529) will create a file that looks like a block device (i.e. a whole file system)

```bash
dd if=/dev/zero of=blah.img bs=1M count=256
mke2fs blah.img
mkdir blah_subdir
mount -o loop blah.img blah_subdir
# will show up as `/dev/loop` something
# add files etc
gzip blah.img # gzip image
```

* [usb flash file systems have problems and need special treatment to do with erase block size](https://youtu.be/Sk9TatW9ino?t=3746)
* [start of intro to mkroot](https://youtu.be/Sk9TatW9ino?t=4115)
* [mkroot walkthrough](https://youtu.be/Sk9TatW9ino?t=4380)
* [Standard Linux directories](https://youtu.be/Sk9TatW9ino?t=4837)
* [Start of discussion about `init`](https://youtu.be/Sk9TatW9ino?t=5047)
* [PID 1 and `init`, why it's special](https://youtu.be/Sk9TatW9ino?t=5155)
* ["oneit" Rob]((https://youtu.be/Sk9TatW9ino?t=5308)) [oneit](https://github.com/landley/toybox/blob/master/toys/other/oneit.c)
* [devtmpfs and devpts](https://youtu.be/Sk9TatW9ino?t=5415) to populate the `/dev` directory with the devices and `/dev/pts` with psuedo terminals  (don't need udev or systemd as the kernel does it)
* [more stuff about consoles, contolling ttys, signals and `oneit`](https://youtu.be/Sk9TatW9ino?t=5555)
* [QEMU and inputting enviromental variables from the its command line](https://youtu.be/Sk9TatW9ino?t=5700)
* [`/etc/passwd` & `/etc/group` discussion](https://youtu.be/Sk9TatW9ino?t=5770)
* [Miniconfig](https://youtu.be/Sk9TatW9ino?t=6453) [KCONFIG_ALLCONFIG=mini.conf](https://www.kernel.org/doc/Documentation/kbuild/kconfig.txt)
* [Kernel building](https://youtu.be/Sk9TatW9ino?t=6820)
* [Linux kernel config](https://github.com/landley/aboriginal/blob/master/sources/baseconfig-linux)
* [Minimal config for kernel (e.g. ARM)](https://github.com/landley/aboriginal/blob/master/sources/targets/armv6l)

## Get mkroot

```bash
git clone https://github.com/landley/mkroot
less mkroot/README # instructions
```

need to install suitable packages on the starter system

```bash
pacman -S qemu cpio bc # may not need base-devel musl
```

download native compiler from [musl libc cross compiler for mkroot](https://mkroot.musl.cc/latest)
Extract the native compiler in a suitable directory

```bash
mkdir ccc
cd ccc
wget https://mkroot.musl.cc/latest/x86_64-linux-musl-native.tgz
bsdtar xvf x86_64-linux-musl-native.tgz
ln -s ~/mkroot/mcm ~/ccc
```

[if something's missing, like bc](https://github.com/landley/mkroot/issues/2)

```bash
pacman -S bc
rm -rf airlock
./cross.sh x86_64 ./mkroot.sh HOST_EXTRA='bc'
```

### Skinny Distributions

#### Probably Working

* [Alpine Linux](https://alpinelinux.org)
* [Welcome to Adélie Linux](https://www.adelielinux.org)
* [KISS - home](https://k1ss.org)
* [Compare Adélie Linux to other distros](https://www.adelielinux.org/about/compare.html)

#### Experimental

* [glaucus Linux - someone building a whole minimal distribution based on Toolbox and the ideas of LFS](https://github.com/glaucuslinux/glaucus)
* [Musl-LFS: Linux From Scratch using Musl as Libc](https://github.com/dslm4515/Musl-LFS)
* [oasis is a small linux system](https://github.com/oasislinux/oasis)

## Links

* [Introducing initramfs](http://landley.net/writing/rootfs-intro.html)
* [Tech Tip: How to use initramfs](http://landley.net/writing/rootfs-howto.html)
* [Programming for Initramfs](http://landley.net/writing/rootfs-programming.html)

* [LinuxCommand.org: Learn The Linux Command Line. Write Shell Scripts.](http://linuxcommand.org/index.php)
* [Bash scripting cheatsheet](https://devhints.io/bash)

* [Rob’s blog](http://landley.net/notes.html)
* [Stuff Rob's written.](http://landley.net/writing/)

* [J-Core Open Processor](https://j-core.org/)
* [j-core mailing list](https://lists.j-core.org/mailman/listinfo/j-core)
* [Dropbear SSH](https://matt.ucc.asn.au/dropbear/dropbear.html) & [github for it](https://github.com/mkj/dropbear)

* [mkroot - simple linux system builder, bootable under qemu for multiple architectures.](https://github.com/landley/mkroot)
* [Blog about successor to Aboriginal Linux](https://landley.net/notes-2016.html#17-05-2016)
* [beginnings of mkroot](http://lists.landley.net/pipermail/mkroot-landley.net/2017-May/000000.html)

* [Firmware Linux history, predecessor to Aboriginal Linux, lots of useful stuff](http://www.landley.net/aboriginal/history.html)

* [Using and internal workings of Aboriginal Linux](http://www.landley.net/aboriginal/README)
* [About Aboriginal Linux](http://www.landley.net/aboriginal/about.html)
* [Aboriginal Linux build stages](http://www.landley.net/aboriginal/build-stages.html)

* [Linux bootdisk howto](http://tldp.org/HOWTO/Bootdisk-HOWTO/index.html)
* [User Mode Linux, run linux inside linux](http://landley.net/writing/docs/UML.html)

* [arch linux BusyBox](https://wiki.archlinux.org/index.php/BusyBox)
* [musl libc](https://www.musl-libc.org/)
* [Write messages to stdout from anywhere, by modifying pl011_console_putchar](https://github.com/torvalds/linux/blob/master/drivers/tty/serial/amba-pl011.c)
* [Toybox vs BusyBox - Rob Landley, hobbyist](https://www.youtube.com/watch?v=MkJkyMuBm3g)

<!-- markdownlint-disable MD034 -->
* (https://en.wikipedia.org/wiki/Linux_startup_process)
* (https://en.wikipedia.org/wiki/Initial_ramdisk)
* (https://wiki.archlinux.org/index.php/Arch_boot_process)
* (https://wiki.archlinux.org/index.php/EFISTUB)
* (https://wiki.archlinux.org/index.php/Microcode#EFISTUB)
* (https://glowingthumb.com/uefi-shell-scripts-3-of-3/)
<!-- markdownlint-enable MD034 -->
