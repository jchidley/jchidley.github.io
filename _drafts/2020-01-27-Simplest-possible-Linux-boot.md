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

t=160 

* Kernel - e.g, Linux
* C library - musl libc 
* Toolchain - compiler, linker, etc
* Command-Line utilities - busybox, toybox

[Aboringinal Linux, and the actual 7 packages required](https://www.youtube.com/watch?v=Sk9TatW9ino&feature=youtu.be&t=225) [GitHub source](https://github.com/landley/aboriginal)

[Linux print statements, from anywhere at any time](https://youtu.be/Sk9TatW9ino?t=857) Writing to a real serial device (pl011 console putchar) anytime, even during boot, from Linux
[Cross compiling](https://youtu.be/Sk9TatW9ino?t=1095)
[Simple main.c hello world as init](https://youtu.be/Sk9TatW9ino?t=1203)

[Hello World, bare metal](https://youtu.be/Sk9TatW9ino?t=408) [Freedom Embedded: Hello world for bare metal ARM using QEMU ](https://balau82.wordpress.com/2010/02/28/hello-world-for-bare-metal-arm-using-qemu/)
[QEMU Explanation](https://youtu.be/Sk9TatW9ino?t=580)
[Linux Kernel booting](https://youtu.be/Sk9TatW9ino?t=1461) mounting a root file system, cpio archive extracted into initramfs (ramfs/tmpfs) and looks for `init` (previously `linuxrc`)

[Linux File Systems Explanations](https://youtu.be/Sk9TatW9ino?t=1535) Block backed (as used on a disk, like ext2), pipe backed (it’s a program providing data over a protocol like NFS and SAMBA do over a network), RAM backed file system (using a system like the disk cache e.g. ramfs, tmpfs), synthetic file system (proc, sys). `initrd` is a RAM disk is a block backed file system stored in RAM so this also needs a page cache - less efficient than ramfs.

https://youtu.be/Sk9TatW9ino?t=1800 running `init` from top level directory, [linux/init/main.c `start_kernel` function](https://www.youtube.com/watch?v=Sk9TatW9ino&feature=youtu.be&t=1840) and [`kernel_init` function](https://github.com/torvalds/linux/blob/master/init/main.c) has a list of backup places to look fir init, including `/bin/sh`.

https://youtu.be/Sk9TatW9ino?t=1461 what happens during Kernel booting
Boot, mount Linux root file system, can use CPIO archive that is extracted to, say, initramfs or boot from a block device (root= option), run a program called “init”
vmLinux is an ELF format and then some transformation (binary?) to get bzImage
[`initrd` kernel parameter](https://youtu.be/Sk9TatW9ino?t=2040) is designed for block devices but will use `cpio` and extract to `initramfs`.  Also `rdinit` has been used in the past
[Linux kernel command line](https://youtu.be/Sk9TatW9ino?t=2125) required `console=` serial console
https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/Documentation?h=v5.9.6 www.kernel.org, stable, Documentation 
https://www.kernel.org/doc/html/v4.14/admin-guide/kernel-parameters.html 
(busybox addition to init and configuration of)[https://youtu.be/Sk9TatW9ino?t=2400] 
Defconfig is default configuration, `make help` will often tell you the various targets 
[kbuild - What exactly does Linux kernel’s `make defconfig` do? - Stack Overflow](https://stackoverflow.com/questions/41885015/what-exactly-does-linux-kernels-make-defconfig-do)

https://youtu.be/Sk9TatW9ino?t=3496 Repackage a cpio as squashfs or ext2 using [mksquashfs](https://manpages.debian.org/jessie/squashfs-tools/mksquashfs.1.en.html) or [mkfs.ext2](https://linux.die.net/man/8/mkfs.ext2) respectively
Loop back device https://youtu.be/Sk9TatW9ino?t=3529 will create a file that looks like a block device (i.e. a whole file system)

```
dd if=/dev/zero of=blah.img bs=1M count=256
mke2fs blah.img
mkdir blah_subdir
mount -o loop blah.img blah_subdir # can't verifiy this on Windows 10 WSL
# will show up as `/dev/loop` something
# add files etc
gzip blah.img 
# gives a gzip'd image
```


* https://youtu.be/Sk9TatW9ino?t=3746 usb flash file systems have problems and need special treatment to do with erase block size
* https://youtu.be/Sk9TatW9ino?t=4115 start of intro to mkroot
* https://youtu.be/Sk9TatW9ino?t=4380 mkroot walkthrough 
* https://youtu.be/Sk9TatW9ino?t=4837 Standard Linux directories
* https://youtu.be/Sk9TatW9ino?t=5047 Start of discussion about `init` 
* https://youtu.be/Sk9TatW9ino?t=5155 PID 1 and `init`, why it's special 
* https://youtu.be/Sk9TatW9ino?t=5308 “One it” Rob [oneit](https://github.com/landley/toybox/blob/master/toys/other/oneit.c)
* https://youtu.be/Sk9TatW9ino?t=5415 devtmpfs and devpts to populate the `/dev` directory with the devices and `/dev/pts` with psuedo terminals (don't need udev or systemd as the kernel does it)
* https://youtu.be/Sk9TatW9ino?t=5555 more stuff about consoles, contolling ttys, signals and `oneit`
* https://youtu.be/Sk9TatW9ino?t=5700 QEMU and inputting enviromental variables from the its command line
* https://youtu.be/Sk9TatW9ino?t=5770 `/etc/passwd` & `/etc/group` discussion
* https://youtu.be/Sk9TatW9ino?t=6453 Miniconfig 
* https://www.kernel.org/doc/Documentation/kbuild/kconfig.txt KCONFIG_ALLCONFIG=mini.conf
* https://youtu.be/Sk9TatW9ino?t=6820 Kernel building
* https://github.com/landley/aboriginal/blob/master/sources/baseconfig-linux Linux kernel config
* https://github.com/landley/aboriginal/blob/master/sources/targets/armv6l Minimal config for kernel (e.g. ARM)

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

### QEMU Booting Raspberry Pi

https://github.com/dhruvvyas90/qemu-rpi-kernel/tree/master/native-emuation Recent specific instructions for a Raspberry Pi
https://azeria-labs.com/emulate-raspberry-pi-with-qemu/ older but still helpful instructions, especially about mounting partitions
https://stackoverflow.com/questions/1419489/how-to-mount-one-partition-from-an-image-file-that-contains-multiple-partitions how to mount a partition within an image file that contains several
https://blog.sleeplessbeastie.eu/2017/07/03/how-to-use-loop-devices/ useful examples of how to use loop devices
https://landley.net/aboriginal/presentation.html for extra qemu options
in addition to the `qemu` package also needed `qemu-arch-extra` on Arch Linux

For Arch, packages `qemu` and `qemu-arch-extra` are required. The first steps are to download the standard Raspbian images and unzip them.

After unzipping the Raspbian download to a img file, I needed to use 

```
fdisk -u sectors -l ../Downloads/2020-08-20-raspios-buster-armhf-lite.img
```

to work out the correct options to setup a loop device.  This showed that the first partitions *Start* (in sectors) was 8192 and *Sectors* was 524288.  So the *offset* in bytes will be 8192 * 512 and the *sizelimit* 524288 * 512

```
losetup -f —show -P —offset $((8192 * 512)) —sizelimit $((524288 * 512))  ../Downloads/2020-08-20-raspios-buster-armhf-lite.img
mkdir /mnt/rpi
mount /dev/loop0 /mnt/rpi
mkdir rpi_qemu
cd rpi_qemu
cp /mnt/rpi/kernel* .
cp /mnt/rpi/*.dtb .
umount /mnt/rpi
losetup -d /dev/loop0 # or the correct loop
```

`qemu-system-aarch64` kept complaining that the image was in the raw format, and I couldn't work how to specify the format for the `-sd` option, I converted the raspbian image from a *raw* format to the *qcow2* one using 

```
qemu-img convert -f raw -O qcow2 ../Downloads/2020-08-20-raspios-buster-armhf-lite.img rpi.qcow2
```

Finally, my modified command to start the image was:

```
qemu-system-aarch64 -M raspi3 -append "rw earlyprintk loglevel=8 console=ttyAMA0,115200 dwc_otg.lpm_enable=0 root=/dev/mmcblk0p2 rootdelay=1" -dtb ./bcm2710-rpi-3-b-plus.dtb -sd rpi.qcow2 -kernel kernel8.img -m 1G -smp 4 -serial stdio -usb -device usb-mouse -device usb-kbd
```

I don't need a graphics terminal so `-nographic` and adjusting `-serial mon:stdio` which also allows scripting and cut and paste to the terminal, apparently.  Currently on shutdown the kernel panics leading to a hang requiring me to manually kill the qemu command. Adding `-no-reboot` and `panic=1` to "-append 'OPTIONS'" is supposed to fix this.

https://stackoverflow.com/questions/61562014/qemu-kernel-for-raspberry-pi-3-with-networking-and-virtio-support 
“The latest versions of QEMU (5.1.0 and 5.0.1) have USB emulation for the raspi3 machine (qemu-system-aarch64 -M raspi3).

You can emulate networking and access to SSH if you use: -device usb-net,netdev=net0 -netdev user,id=net0,hostfwd=tcp::5555-:22 in QEMU”

```
qemu-system-aarch64 -m 1024 -M raspi3 -kernel kernel8.img -dtb bcm2710-rpi-3-b-plus.dtb -sd 2020-08-20-raspios-buster-armhf.img -append “console=ttyAMA0 root=/dev/mmcblk0p2 rw rootwait rootfstype=ext4” -nographic -device usb-net,netdev=net0 -netdev user,id=net0,hostfwd=tcp::5555-:22
```

* [Bare metal Raspberry Pi 3 tutorials](https://github.com/bztsrc/raspi3-tutorial) this guy submitted the patch to qemu to get raspi3 working (raspi2 is apparently from Microsoft)
* [Raspberry Pi ARM based bare metal examples](https://github.com/dwelch67/raspberrypi)
* [Learning operating system development using Linux kernel and Raspberry Pi](https://github.com/s-matyukevich/raspberry-pi-os)
* [RPI3 QEMU - Raspberry Pi Forums](https://www.raspberrypi.org/forums/viewtopic.php?f=72&t=195565&sid=030b9410f3f3172af333d2eea90a2646) more information and extra patches
* [Raspberry Pi 4 and QEMU (x86/x64) - Raspberry Pi Forums](https://www.raspberrypi.org/forums/viewtopic.php?t=246886) running emu on the pi and emulating x86/x64.  Note that we I compiled from source and cross compiling
* [Run another OS on your RPi3 as a virtualized QEMU guest under KVM (64-bit) - Raspberry Pi Forums](https://www.raspberrypi.org/forums/viewtopic.php?t=224057)
* [Using QEMU to emulate a Raspberry Pi](https://blog.agchapman.com/using-qemu-to-emulate-a-raspberry-pi/)


### distcc 

* [GitHub - distcc/distcc: distributed builds for C, C++ and Objective C](https://github.com/distcc/distcc) [distcc: a fast, free distributed C/C++ compiler](https://distcc.github.io) 
* [Raspberry Pi Toolchain](https://github.com/raspberrypi/tools) needed on the various host computers
* [Distributed Compiling with distcc » Raspberry Pi Geek](https://www.raspberry-pi-geek.com/Archive/2016/17/Distributed-software-compilation-for-the-Raspberry-Pi)
* [Building for Raspberry Pi using distcc - Kvaser](https://www.kvaser.com/developer-blog/building-raspberry-pi-using-distcc/)
* [Raspberry Pi/Cross building - Gentoo Wiki](https://wiki.gentoo.org/wiki/Raspberry_Pi/Cross_building)
* [raspberry pi and distcc | openFrameworks](https://openframeworks.cc/setup/raspberrypi/raspberry-pi-distcc-guide/)
* [Using a Raspberry Pi as a distcc node · Random kit](https://jtanx.github.io/2019/04/19/rpi-distcc-node/) using a Pi as a node for x86 compilation 
* [Using distcc for faster builds - Raspberry Pi Forums](https://www.raspberrypi.org/forums/viewtopic.php?t=60908)


## Links

* [Introducing initramfs](http://landley.net/writing/rootfs-intro.html)
* [Tech Tip: How to use initramfs](http://landley.net/writing/rootfs-howto.html)
* [Programming for Initramfs](http://landley.net/writing/rootfs-programming.html)
* [LinuxCommand.org: Learn The Linux Command Line. Write Shell Scripts.](http://linuxcommand.org/index.php)
* [Bash scripting cheatsheet](https://devhints.io/bash)

* [rob’s blog](http://landley.net/notes.html)
* [Stuff I’ve written.](http://landley.net/writing/)

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

* [Developing using QEMU](http://www.landley.net/aboriginal/presentation.html)
* [booting a fresh linux kernel on qemu](https://ops.tips/notes/booting-linux-on-qemu/)
* [How to Build A Custom Linux Kernel For Qemu](https://mgalgs.github.io/2015/05/16/how-to-build-a-custom-linux-kernel-for-qemu-2015-edition.html)
* [Fast linux kernel testing with qemu](http://ncmiller.github.io/2016/05/14/linux-and-qemu.html)
* [Use “ and not ‘ on Qemu on Windows](https://github.com/dhruvvyas90/qemu-rpi-kernel/issues/71)
* [Hello world for bare metal ARM using QEMU](https://balau82.wordpress.com/2010/02/28/hello-world-for-bare-metal-arm-using-qemu/)

* [arch linux BusyBox](https://wiki.archlinux.org/index.php/BusyBox)
* [musl libc](https://www.musl-libc.org/)
* [Write messages to stdout from anywhere, by modifying pl011_console_putchar](https://github.com/torvalds/linux/blob/master/drivers/tty/serial/amba-pl011.c)
* [glaucus Linux - someone building a whole minimal distribution based on Toolbox and the ideas of LFS]https://github.com/glaucuslinux/glaucus
* [Toybox vs BusyBox - Rob Landley, hobbyist](https://www.youtube.com/watch?v=MkJkyMuBm3g)

<!-- markdownlint-disable MD034 -->
* (https://en.wikipedia.org/wiki/Linux_startup_process)
* (https://en.wikipedia.org/wiki/Initial_ramdisk)
* (https://wiki.archlinux.org/index.php/Arch_boot_process)
* (https://wiki.archlinux.org/index.php/EFISTUB)
* (https://wiki.archlinux.org/index.php/Microcode#EFISTUB)
* (https://glowingthumb.com/uefi-shell-scripts-3-of-3/)
<!-- markdownlint-enable MD034 -->
