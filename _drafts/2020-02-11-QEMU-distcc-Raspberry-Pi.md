---
date: "2020-02-11"
title: "QEMU distcc Raspberry Pi"
---
<!-- 2020-02-11-QEMU-Raspberry-Pi.md -->

<!-- markdownlint-disable MD025 -->
# URL Dump
<!-- markdownlint-enable MD025 -->

## Introduction

### QEMU Booting Raspberry Pi

* [Native emulation of Rpi2/3 using Qemu's Raspi2/3 machine](https://github.com/dhruvvyas90/qemu-rpi-kernel/tree/master/native-emuation) Recent specific instructions for a Raspberry Pi
* [Raspberry Pi on QEMU](https://azeria-labs.com/emulate-raspberry-pi-with-qemu/) older but still helpful instructions, especially about mounting * partitions
* [How to mount one partition from an image file that contains multiple partitions on Linux?](https://stackoverflow.com/questions/1419489/how-to-mount-one-partition-from-an-image-file-that-contains-multiple-partitions) how to mount a partition * within an image file that contains several
* [How to use loop devices](https://blog.sleeplessbeastie.eu/2017/07/03/how-to-use-loop-devices/) useful examples of how to use loop devices
* [Developing for non-x86 targets using QEMU](https://landley.net/aboriginal/presentation.html) for extra qemu options
in addition to the `qemu` package also needed `qemu-arch-extra` on Arch Linux

* [QEMU Documentation/Platforms/ARM](https://wiki.qemu.org/Documentation/Platforms/ARM#Generic_ARM_system_emulation_with_the_virt_machine)
* [Virtual 32 bit QEMU](https://translatedcode.wordpress.com/2016/11/03/installing-debian-on-qemus-32-bit-arm-virt-board/)
* [Installing Debian on QEMU’s 64-bit ARM “virt” board](https://translatedcode.wordpress.com/2017/07/24/installing-debian-on-qemus-64-bit-arm-virt-board/* )
* [Debian on QEMU’s Raspberry Pi 3 model - flaky](https://translatedcode.wordpress.com/2018/04/25/debian-on-qemus-raspberry-pi-3-model/)
* [Raspbian “stretch” for Raspberry Pi 3 on QEMU - February 2019](https://github.com/wimvanderbauwhede/limited-systems/wiki/Raspbian-%22stretch%22-for-Raspberry-Pi-3-on-QEMU)
* [Windows for Raspberry Pi 2 on QEMU HOWTO - June 2018 but older](https://github.com/0xabu/qemu/wiki)
* [Run a virtualized image of Raspberry Pi in QEMU - April 2018](https://tkrel.com/7390)
* [Emulate Raspberry PI with QEMU - April 2018](http://blog.hellonico.info/iot/arm_on_qemu/)
* [How to emulate Ubuntu Core for Raspberry Pi 3 using QEMU? - March 2018](https://stackoverflow.com/questions/49134948/how-to-emulate-ubuntu-core-for-raspberry-pi-3-using-qemu)
* [How to emulate the Raspberry Pi 2 on QEMU?- March 2015](https://stackoverflow.com/questions/28880833/how-to-emulate-the-raspberry-pi-2-on-qemu)
* [Emulate Rapberry Pi 2 in QEMU - November 2015](https://blog.3mdeb.com/2015/2015-12-30-emulate-rapberry-pi-2-in-qemu/)

For Arch, packages `qemu` and `qemu-arch-extra` are required. The first steps are to download the standard Raspbian images and unzip them.

After unzipping the Raspbian download to a img file, I needed to use

```bash
fdisk -u sectors -l ../Downloads/2020-08-20-raspios-buster-armhf-lite.img
```

to work out the correct options to setup a loop device.  This showed that the first partitions *Start* (in sectors) was 8192 and *Sectors* was 524288.  So the *offset* in bytes will be 8192 * 512 and the *sizelimit* 524288 * 512

[How to use loop devices](https://sleeplessbeastie.eu/2017/07/03/how-to-use-loop-devices/)

```bash
losetup -f —show -P —offset $((8192 * 512)) —sizelimit $((524288 * 512)) ../Downloads/2020-08-20-raspios-buster-armhf-lite.img
mount /dev/loop0 /mnt/rpi # or the appropriate loop device
```

Or do the mount directly like this:

`mount 2020-08-20-raspios-buster-armhf-lite.img /mnt/rpi/ -o loop,offset=${OFFSET_of_PARTITION},sizelimit=$((524288 * 512))`

Note: I have chopped this up somehow - this was correct in simplest file a few updates back. Needs testing


```bash
mkdir rpi_qemu
cd rpi_qemu
cp /mnt/rpi/kernel* .
cp /mnt/rpi/*.dtb .
umount /mnt/rpi
losetup -d /dev/loop0 # or the correct loop
```

`qemu-system-aarch64` kept complaining that the image was in the raw format, and I couldn't work how to specify the format for the `-sd` option, I converted the raspbian image from a *raw* format to the *qcow2* one using

```bash
qemu-img convert -f raw -O qcow2 ../Downloads/2020-08-20-raspios-buster-armhf-lite.img rpi.qcow2
```

Finally, my modified command to start the image was:

```bash
qemu-system-aarch64 -M raspi3 -append "rw earlyprintk loglevel=8 console=ttyAMA0,115200 dwc_otg.lpm_enable=0 root=/dev/mmcblk0p2 rootdelay=1" -dtb ./bcm2710-rpi-3-b-plus.dtb -sd rpi.qcow2 -kernel kernel8.img -m 1G -smp 4 -serial stdio -usb -device usb-mouse -device usb-kbd
```

I don't need a graphics terminal so `-nographic` and adjusting `-serial mon:stdio` which also allows scripting and cut and paste to the terminal, apparently.  Currently on shutdown the kernel panics leading to a hang requiring me to manually kill the qemu command. Adding `-no-reboot` and `panic=1` to "-append 'OPTIONS'" is supposed to fix this.

[QEMU kernel for raspberry pi 3 with networking and virtio support](https://stackoverflow.com/questions/61562014/qemu-kernel-for-raspberry-pi-3-with-networking-and-virtio-support) “The latest versions of QEMU (5.1.0 and 5.0.1) have USB emulation for the raspi3 machine (qemu-system-aarch64 -M raspi3).

You can emulate networking and access to SSH if you use: -device usb-net,netdev=net0 -netdev user,id=net0,hostfwd=tcp::5555-:22 in QEMU”

```bash
qemu-system-aarch64 -m 1024 -M raspi3 -kernel kernel8.img -dtb bcm2710-rpi-3-b-plus.dtb -sd 2020-08-20-raspios-buster-armhf.img -append “console=ttyAMA0 root=/dev/mmcblk0p2 rw rootwait rootfstype=ext4” -nographic -device usb-net,netdev=net0 -netdev user,id=net0,hostfwd=tcp::5555-:22
```

* [Bare metal Raspberry Pi 3 tutorials](https://github.com/bztsrc/raspi3-tutorial) this guy submitted the patch to qemu to get raspi3 working (raspi2 is apparently from Microsoft)
* [Raspberry Pi ARM based bare metal examples](https://github.com/dwelch67/raspberrypi)
* [Learning operating system development using Linux kernel and Raspberry Pi](https://github.com/s-matyukevich/raspberry-pi-os)
* [RPI3 QEMU - Raspberry Pi Forums](https://www.raspberrypi.org/forums/viewtopic.php?f=72&t=195565&sid=030b9410f3f3172af333d2eea90a2646) more information and extra patches
* [Raspberry Pi 4 and QEMU (x86/x64) - Raspberry Pi Forums](https://www.raspberrypi.org/forums/viewtopic.php?t=246886) running emu on the pi and emulating x86/x64.  Note that we I compiled from source and cross compiling
* [Run another OS on your RPi3 as a virtualized QEMU guest under KVM (64-bit) - Raspberry Pi Forums](https://www.raspberrypi.org/forums/viewtopic.php?t=224057)
* [Using QEMU to emulate a Raspberry Pi](https://blog.agchapman.com/using-qemu-to-emulate-a-raspberry-pi/)
* [QEMU Documentation/Platforms/ARM](https://wiki.qemu.org/Documentation/Platforms/ARM#Generic_ARM_system_emulation_with_the_virt_machine)
* [Virtual 32 bit QEMU](https://translatedcode.wordpress.com/2016/11/03/installing-debian-on-qemus-32-bit-arm-virt-board/)
* [Installing Debian on QEMU’s 64-bit ARM "virt" board](https://translatedcode.wordpress.com/2017/07/24/installing-debian-on-qemus-64-bit-arm-virt-board/* )
* [Debian on QEMU’s Raspberry Pi 3 model - flaky](https://translatedcode.wordpress.com/2018/04/25/debian-on-qemus-raspberry-pi-3-model/)
* [Raspbian "stretch" for Raspberry Pi 3 on QEMU - February 2019](https://github.com/wimvanderbauwhede/limited-systems/wiki/Raspbian-%22stretch%22-for-Raspberry-Pi-3-on-QEMU)
* [Windows for Raspberry Pi 2 on QEMU HOWTO - June 2018 but older](https://github.com/0xabu/qemu/wiki)
* [Run a virtualized image of Raspberry Pi in QEMU - April 2018](https://tkrel.com/7390)
* [Emulate Raspberry PI with QEMU - April 2018](http://blog.hellonico.info/iot/arm_on_qemu/)
* [How to emulate Ubuntu Core for Raspberry Pi 3 using QEMU? - March 2018](https://stackoverflow.com/questions/49134948/how-to-emulate-ubuntu-core-for-raspberry-pi-3-using-qemu)
* [How to emulate the Raspberry Pi 2 on QEMU?- March 2015](https://stackoverflow.com/questions/28880833/how-to-emulate-the-raspberry-pi-2-on-qemu)
* [Emulate Rapberry Pi 2 in QEMU - November 2015](https://blog.3mdeb.com/2015/2015-12-30-emulate-rapberry-pi-2-in-qemu/)

### distcc

* [GitHub - distcc/distcc: distributed builds for C, C++ and Objective C](https://github.com/distcc/distcc) [distcc: a fast, free distributed C/C++ compiler](https://distcc.github.io)
* [Raspberry Pi Toolchain](https://github.com/raspberrypi/tools) needed on the various host computers
* [Distributed Compiling with distcc » Raspberry Pi Geek](https://www.raspberry-pi-geek.com/Archive/2016/17/Distributed-software-compilation-for-the-Raspberry-Pi)
* [Building for Raspberry Pi using distcc - Kvaser](https://www.kvaser.com/developer-blog/building-raspberry-pi-using-distcc/)
* [Raspberry Pi/Cross building - Gentoo Wiki](https://wiki.gentoo.org/wiki/Raspberry_Pi/Cross_building)
* [raspberry pi and distcc | openFrameworks](https://openframeworks.cc/setup/raspberrypi/raspberry-pi-distcc-guide/)
* [Using a Raspberry Pi as a distcc node · Random kit](https://jtanx.github.io/2019/04/19/rpi-distcc-node/) using a Pi as a node for x86 compilation
* [Using distcc for faster builds - Raspberry Pi Forums](https://www.raspberrypi.org/forums/viewtopic.php?t=60908)

### Links
<!-- markdownlint-disable MD034 -->

* [Developing using QEMU](http://www.landley.net/aboriginal/presentation.html)
* [booting a fresh linux kernel on qemu](https://ops.tips/notes/booting-linux-on-qemu/)
* [How to Build A Custom Linux Kernel For Qemu](https://mgalgs.github.io/2015/05/16/how-to-build-a-custom-linux-kernel-for-qemu-2015-edition.html)
* [Fast linux kernel testing with qemu](http://ncmiller.github.io/2016/05/14/linux-and-qemu.html)
* [Use “ and not ‘ on Qemu on Windows](https://github.com/dhruvvyas90/qemu-rpi-kernel/issues/71)
* [Hello world for bare metal ARM using QEMU](https://balau82.wordpress.com/2010/02/28/hello-world-for-bare-metal-arm-using-qemu/)

* [Pi Linux From Scratch - PiLFS - QEMU](https://intestinate.com/pilfs/beyond.html#qemuuser)

<!-- markdownlint-enable MD034 -->
