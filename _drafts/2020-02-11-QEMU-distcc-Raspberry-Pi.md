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

* [Native emulation of Rpi2/3 using Qemu's Raspi2/3 machine](https://github.com/dhruvvyas90/qemu-rpi-kernel/tree/master/native-emulation) Recent specific instructions for a Raspberry Pi
* [Emulating raspberry pi 4 with qemu - Stack Overflow](https://stackoverflow.com/questions/67045438/emulating-raspberry-pi-4-with-qemu/67056324#67056324)
* [Raspberry Pi on QEMU](https://azeria-labs.com/emulate-raspberry-pi-with-qemu/) older but still helpful instructions, especially about mounting partitions
* [How to mount one partition from an image file that contains multiple partitions on Linux?](https://stackoverflow.com/questions/1419489/how-to-mount-one-partition-from-an-image-file-that-contains-multiple-partitions) 
* [How to use loop devices](https://blog.sleeplessbeastie.eu/2017/07/03/how-to-use-loop-devices/) useful examples of how to use loop devices
* [Developing for non-x86 targets using QEMU](https://landley.net/aboriginal/presentation.html) for extra qemu options in addition to the `qemu` package also needed `qemu-arch-extra` on Arch Linux

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
qemu-system-aarch64\
    -M raspi3\
    -append "rw earlyprintk loglevel=8 console=ttyAMA0,115200 dwc_otg.lpm_enable=0 root=/dev/mmcblk0p2 rootdelay=1"\
    -dtb ./bcm2710-rpi-3-b-plus.dtb\
    -sd rpi.qcow2\
    -kernel kernel8.img\
    -m 1G\
    -smp 4\
    -serial stdio\
    -usb -device usb-mouse -device usb-kbd
```

`qemu-img resize 2022-07-20-jack-lite-qemu.img 8G`

```bash
qemu-system-aarch64\
    -M raspi3b\
    -append "rw earlyprintk loglevel=8 console=ttyAMA0,115200 dwc_otg.lpm_enable=0 root=/dev/mmcblk0p2 rootdelay=1"\
    -dtb .dtb/bcm2710-rpi-3-b-plus.dtb\
    -drive file=./2022-07-20-jack-lite-qemu.img,format=raw,id=sd \
    -kernel kernel8.img\
    -m 1G\
    -smp 4\
    -serial stdio\
    -usb -device usb-mouse -device usb-kbd\
    -nographic
    -device usb-net,netdev=net0 -netdev user,id=net0,hostfwd=tcp::5555-:22
```

```bash
qemu-system-aarch64 \
    -kernel ./kernel8.img \
    -dtb ./bcm2710-rpi-3-b.dtb \
    -M raspi3 -m 1024 \
    -serial mon:stdio \
    -append \"console=ttyAMA0 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait rw\" \
    -drive file=./raspbian-buster.img,format=raw,id=sd \
    -no-reboot
    -nographic
```

sudo qemu-system-aarch64 -M raspi3b -dtb boot/bcm2710-rpi-3-b-plus.dtb -drive file=deploy/2022-07-20-jack-lite-qemu.img,format=raw,id=sd -kernel boot/kernel8.img -m 1G -nographic -serial mon:stdio -append "console=ttyAMA0 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait rw"


sudo qemu-system-aarch64 -M raspi3b -dtb boot/bcm2710-rpi-3-b-plus.dtb -drive file=deploy/2022-07-20-jack-lite-qemu.img,format=raw,id=sd -kernel boot/kernel8.img -m 1G -usb -device usb-mouse -device usb-kbd -nographic -serial mon:stdio -device usb-net,netdev=net0 -netdev user,id=net0,hostfwd=tcp::5555-:22 -append "console=ttyAMA0 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait rw"


console=serial0,115200 console=tty1 root=ROOTDEV rootfstype=ext4 fsck.repair=yes rootwait quiet init=/usr/lib/raspi-config/init_resize.sh

Changing /etc/fstab entries for /boot and / to /dev/mmcblk0p1 and /dev/mmcblk0p2, respectively. This is instead of using /dev/sda1 & /dev/sda2, respectively as mentioned in some of the tutorials I posted in a previous post. Also do not use PARTUUID entries

[Using QEMU to emulate a Raspberry Pi](https://blog.agchapman.com/using-qemu-to-emulate-a-raspberry-pi/)

I don't need a graphics terminal so `-nographic` and adjusting `-serial mon:stdio` which also allows scripting and cut and paste to the terminal, apparently.  Currently on shutdown the kernel panics leading to a hang requiring me to manually kill the qemu command. Adding `-no-reboot` and `panic=1` to "-append 'OPTIONS'" is supposed to fix this.

[QEMU kernel for raspberry pi 3 with networking and virtio support](https://stackoverflow.com/questions/61562014/qemu-kernel-for-raspberry-pi-3-with-networking-and-virtio-support) “The latest versions of QEMU (5.1.0 and 5.0.1) have USB emulation for the raspi3 machine (qemu-system-aarch64 -M raspi3).

You can emulate networking and access to SSH if you use: -device usb-net,netdev=net0 -netdev user,id=net0,hostfwd=tcp::5555-:22 in QEMU”

```bash
qemu-system-aarch64 \
    -m 1024 \
    -M raspi3 \
    -kernel kernel8.img \
    -dtb bcm2710-rpi-3-b-plus.dtb \
    -sd 2020-08-20-raspios-buster-armhf.img \
    -append “console=ttyAMA0 root=/dev/mmcblk0p2 rw rootwait rootfstype=ext4” \
    -nographic \
    -device usb-net,netdev=net0 -netdev user,id=net0,hostfwd=tcp::5555-:22
```

[Developing for non-x86 targets using QEMU](https://landley.net/aboriginal/presentation.html#qemu_options)
[Raspberry Pi boards (raspi0, raspi1ap, raspi2b, raspi3ap, raspi3b) -- QEMU documentation](https://www.qemu.org/docs/master/system/arm/raspi.html)
[raspbian lite - No video output running on QEMU - Raspberry Pi Stack Exchange](https://raspberrypi.stackexchange.com/questions/136368/no-video-output-running-on-qemu)

```bash
sudo qemu-system-aarch64 \
    -M raspi3b \
    -append "rw earlyprintk loglevel=8 console=ttyAMA0,115200 root=/dev/mmcblk0p2 rootdelay=1" \
    -dtb bcm2710-rpi-3-b.dtb \
    -sd 2022-01-28-raspios-bullseye-armhf-lite.img \
    -kernel kernel8.img \
    -m 1G \
    -smp 4 \
    -usb -device usb-mouse -device usb-kbd \
    -device usb-net,netdev=net0 \
    -netdev user,id=net0,hostfwd=tcp::5555-:22
``` 

[boot - Running raspbian buster with qemu - Raspberry Pi Stack Exchange](https://raspberrypi.stackexchange.com/questions/100384/running-raspbian-buster-with-qemu)
[Debian "buster" for Raspberry Pi 3 on QEMU · wimvanderbauwhede/limited-systems Wiki · GitHub](https://github.com/wimvanderbauwhede/limited-systems/wiki/Debian-%22buster%22-for-Raspberry-Pi-3-on-QEMU)

```bash
qemu-system-aarch64 \
    -M raspi3 \
    -append "rw earlyprintk=ttyAMA0,115200 loglevel=8 console=ttyAMA0,115200 root=PARTUUID=6c586e13-02 rootfstype=ext4 rootwait" \
    -cpu cortex-a53 \
    -dtb /path/to/bcm2710-rpi-3-b.dtb \
    -drive id=hd-root,file=/path/to/2019-09-26-raspbian-buster-lite.img,format=raw \
    -show-cursor \
    -kernel /path/to/kernel8.img \
    -m 1024 \
    -serial mon:stdio \
    -nographic
``` 

Answer here is to use the `virt` emulation
[virtual machine - Trying to run Raspberry-Pi image under QEMU, but VM memory is limited to 256MB - Stack Overflow](https://stackoverflow.com/questions/69143721/trying-to-run-raspberry-pi-image-under-qemu-but-vm-memory-is-limited-to-256mb)

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

### Compiling Qemu

[Hosts/Linux - QEMU](https://wiki.qemu.org/Hosts/Linux)
[QEMU / QEMU · GitLab](https://gitlab.com/qemu-project/qemu)

```bash
git clone https://gitlab.com/qemu-project/qemu.git
cd qemu
./configure --help
# Configure QEMU for aarch64 only - faster build
./configure --target-list=aarch64-softmmu
# Build in parallel - my system has 4 CPUs
make -j4
```

```bash
./configure --target-list=aarch64-softmmu arm-softmmu x86_64-softmmu
```

[Building QEMU 5.0 on Raspbian | www.chrisrcook.com](https://www.chrisrcook.com/projects/building-qemu-5-0-on-raspbian/)
[Running Alpine Linux in QEMU - Yuankun's Blog](https://yuankun.me/posts/running-alpine-linux-in-qemu/)
[Hosts/Linux - QEMU](https://wiki.qemu.org/Hosts/Linux)
[QEMU - Alpine Linux](https://wiki.alpinelinux.org/wiki/QEMU#Using_Xorg_inside_QEMU)

[[SOLVED] Qemu 5.0.0 alien build crashes trying to boot Raspbian-Buster as a RPi3](https://www.linuxquestions.org/questions/slackware-14/qemu-5-0-0-alien-build-crashes-trying-to-boot-raspbian-buster-as-a-rpi3-4175680027/#post6157331)

"
So after much testing and searching, I've come up with a solution to this problem.
I'll document it here in the event that anyone else encounters this problem.

There are a few things that resulted in success:

- Building Qemu with the --disable-tcg-interpreter flag; Alien's slackbuild script uses the --enable-tcg-interpreter flag (approx line 341 of qemu.SlackBuild script) so this needs to be changed manually. Otherwise you will eventually encounter the 'tcg fatal error' mentioned in my original post.

- Changing /etc/fstab entries for /boot and / to /dev/mmcblk0p1 and /dev/mmcblk0p2, respectively. This is instead of using /dev/sda1 & /dev/sda2, respectively as mentioned in some of the tutorials I posted in a previous post. Also do not use PARTUUID entries.

- Changing root=/dev/mmcblk0p2 in the 'append' line for Qemu itself (see complete command below)

- Note that Raspbian/RaspberrryPiOS's cmdline.txt in /boot provides the initial kernel 'append' used when booting the OS for the first time. It explicitly calls a script (/usr/lib/raspi-config/init_resize.sh) using an init= argument that does some checks and resizes the root filesystem to the available size of the disk/SD card it is installed on. The script also removes itself from the /boot/cmdline.txt file after it has (successfully) run so that it doesn't try and resize the root partition again every time you power on your Pi.
I, however, made additional partitions on my image to my own custom specifications, and upon running init_resize.sh the script started complaining about unsupported partitions, so I tried booting without the script and it booted just fine.
I would probably omit this from Qemu's append line. If run under Qemu, and if successful, it will remove it's invocation from cmdline.txt. As a result, once you flash the image to an SD card and run it on an actual Pi, this script won't be run and won't resize it's root partition to the available size of your SD card.

- Also note that I had previously mounted the image locally and extracted both the kernel and dtb files from /boot and passed them to Qemu.

- Somewhere along my travels I found a post suggesting to comment-out everything in /usr/lib/ld.so.preload, but doing that is what ultimately lead to the 'tcg fatal error' from my original post. I left it un-commented and after rebuilding Qemu with the tcg interpreter disabled, everything ran fine.

My final Qemu command is:

```bash
qemu-system-aarch64 \
    -kernel ./kernel8.img \
    -dtb ./bcm2710-rpi-3-b.dtb \
    -M raspi3 -m 1024 \
    -serial mon:stdio \
    -append \"console=ttyAMA0 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait rw\" \
    -drive file=./raspbian-buster.img,format=raw,id=sd \
    -no-reboot
    -nographic
```
 
My /etc/fstab on the Raspbian image is:
```bash
/dev/mmcblk0p1                                  /boot                           vfat    defaults                0       2
/dev/mmcblk0p2                                  /                               ext4    defaults,noatime        0       1

proc                                            /proc                           proc    defaults                0       0
```
"

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
