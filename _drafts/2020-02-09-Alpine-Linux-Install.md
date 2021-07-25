---
date: "2020-02-09"
title: "Alpine Linux Install"
---
<!-- 2020-02-09-Alpine-Linux-Install.md -->

<!-- markdownlint-disable MD025 -->
# Alpine Linux Install
<!-- markdownlint-enable MD025 -->

## Introduction

What makes [Alpine Linux](https://alpinelinux.org/about/) interesting? It is an extremely lightweight and easy to configure system. To really appreaciate just what it offers an administrator look at [these system backup instructions](https://wiki.alpinelinux.org/wiki/Back_Up_a_Flash_Memory_Installation). To build a new system, based on an existing one, take a backup (or use a vanilla [installation file](https://alpinelinux.org/downloads/)), edit or write [the configuration file - AKA apkvol](https://wiki.alpinelinux.org/wiki/Manually_editing_a_existing_apkovl) and add the necessary packages to both [the local cache](https://wiki.alpinelinux.org/wiki/Local_APK_cache) and the `/etc/apk/world` file. `lbu commit` and you are done.

[This guide](https://wiki.alpinelinux.org/wiki/Alpine_Source_Map_by_boot_sequence) describes how Alpine Linux boots and there's a [detailed version for the Raspberry Pi](https://pi3g.com/2019/01/10/alpine-boot-process-on-the-raspberry-pi/). Finally, if you're missing a favourite command then `akp search [faviourite missing command]` is what you need before you `apk add [found package name]`.

For more detailed information see the [Alpine User Handbook](https://docs.alpinelinux.org/user-handbook/0.1a/index.html) and the [Developer Documentation](https://wiki.alpinelinux.org/wiki/Category_talk:Developer_Documentation).

This is the Linux that I have been waiting for.

## From Scratch Install - Intel Desktop

boot USB (or other prepared) boot device and run the setup program

```bash
setup-alpine
```

I manually configured the partitions because I'm running an EFI system.

### EFI boot

create `.nsh` file like this:

```bash
fs0:
cd /alpine1shuttle1
vmlinux ... root... modules... initrd=/alpine1shuttle1/initramfs-lts
```

the boot line is modified from the extlinux.cfg file.  Note the initrd comes at the end and includes the full path on the EFI system drive.

### xfce4 desktop

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

### Firefox

```bash
apk add firefox-esr
```

### The End

This is enough to get a normal desktop in under 2G of disk space.

## From Scratch Install - Raspberry Pi

### On the Build machine

[Install Alpine on a Raspberry Pi](https://wiki.alpinelinux.org/wiki/Raspberry_Pi)
[Classic install or sys mode on Raspberry Pi](https://wiki.alpinelinux.org/wiki/Classic_install_or_sys_mode_on_Raspberry_Pi)

We're going to install Alpine in "diskless" mode and use overlay files.  Prepare an SD card with 500MB DOS bootable partition with the remainder as ext4
[Create suitable partitions programatically](https://superuser.com/questions/332252/how-to-create-and-format-a-partition-using-a-bash-script)

```bash
apk add e2fsprogs lsblk dosfstools
sudo su
cd
PIDEVICE=/dev/sdX # get the correct device from `cat /proc/partitions` or `df -h`
umount ${PIDEVICE}{1,2} # many linuxes automount
# clear the old drive
wipefs -a ${PIDEVICE} #  -a, --all wipe all magic strings (BE CAREFUL!)
# The `sed` script uses the first string of continuous 
# letters and digits after optional spaces, 
# This, in efffect, strips the comments, allowing for in-line comments.
# Note that sending nothing (or spaces) will send a newline
# usually selecting the defaul value.
sed -e 's/\s*\([\+0-9a-zA-Z]*\).*/\1/' << EOF | fdisk ${PIDEVICE}
  o # create a new empty DOS partition table
  n # new partition
  p # primary partition
  1 # partition number 1
    # default: start at beginning of disk 
  +500M # 500 MB boot parttion
  t # change a partition type
  c # change type of partition to 'W95 FAT32 (LBA)'
  n # add a new partition
  p # primary partition
  2 # partion number 2
    # default: start immediately after preceding partition
    # default: extend partition to end of disk
  p # print the partition table
  w # write table to disk and exit
EOF
```

or use `sfdisk`.

```bash
sfdisk ${PIDEVICE} << eof
,$((2048*1024)),c
;
eof
sfdisk -V ${PIDEVICE}
```

```bash
mkfs.fat ${PIDEVICE}1
mkfs.ext2 ${PIDEVICE}2 # unnecessary
# armv7 works on every Pi except the first Model A and Model B
cd ~/Downloads # or /home/username/Downloads
wget https://dl-cdn.alpinelinux.org/alpine/v3.14/releases/armv7/alpine-rpi-3.14.0-armv7.tar.gz
# wget https://dl-cdn.alpinelinux.org/alpine/v3.14/releases/aarch64/alpine-rpi-3.14.0-aarch64.tar.gz # pi 4
tdrive="$(mktemp -d /tmp/alpine_install.XXXXXX)"
mount ${PIDEVICE}1 $tdrive
# download the correct alpine linux from the web site
tar -xvf alpine-rpi-3.14.0-armv7.tar.gz -C $tdrive --no-same-owner
```

To find out the correct options, run `setup-alpine -c answerfile.txt` on a newly booted Alpine system. This script doesn't always work as it should

Things to change

* alpine-scratch-pi # hostname
* chidley.home #local domain name

```bash
cat > $tdrive/answerfile.txt << "EOF"
# Use GB layout with GB variant
KEYMAPOPTS="gb gb"

# Set hostname to alpine-scratch-pi
HOSTNAMEOPTS="-n alpine-scratch-pi"

# Contents of /etc/network/interfaces
INTERFACESOPTS="auto lo
iface lo inet loopback

# Internal Ethernet - WAN
auto eth0
iface eth0 inet dhcp
    hostname alpine-scratch-pi
"

# `home` is the local domain name and 8.8.8.8 Google public nameserver
# or ip address of the local name server
# This will be replaced with custom DNS setup
DNSOPTS="-d chidley.home -n 8.8.8.8"

# Set timezone to UTC
TIMEZONEOPTS="-z UTC"

# set http/ftp proxy
PROXYOPTS="none"

# Use the first mirror, usually CDN (Content Delivery Network)
APKREPOSOPTS="-1"

# Install Dropboar
SSHDOPTS="-c dropbear"

# Use chronyd
NTPOPTS="-c chrony"

# Setup in /media/mmcblk0p1
LBUOPTS="/media/mmcblk0p1"
APKCACHEOPTS="/media/mmcblk0p1/cache"
EOF

sync # make sure all the files are written to the SD card
umount $tdrive
rmdir $tdrive
```

boot

```bash
setup-alpine -f answerfile.txt
# --- check ---
ls /media/mmcblk0p1/cache/ # should have dropbear in it
cat /etc/apk/repositories # should be adjusted from default with, at least:
# /media/mmcblk0p1/apks
# http://uk.alpinelinux.org/alpine/v3.14/main
```

### hardware random number generator

[The HWRNG on the BCM2838 is compatible to iproc-rng200](https://github.com/raspberrypi/linux/commit/577a2fa60481a0563b86cfd5a0237c0582fb66e0)
[Arch Linux Arm: Raspberry Pi](https://archlinuxarm.org/wiki/Raspberry_Pi)

`haveged` competes with the broadcom provided random number generator, now `iproc-rng200` (previously bcm2835_rng and bcm2708-rng) and so it needs to be disabled

```bash
cat /proc/sys/kernel/random/entropy_avail
# typically less than 1000
apk add rng-tools
RNGD_OPTS="-x1 -o /dev/random -r /dev/hwrng"
rc-service rngd start
rc-update add rngd
cat /proc/sys/kernel/random/entropy_avail
# should be more than 3000
rngd -l
# The "Hardware RNG Device (hwrng)" should be an "Available and enabled entropy source"
```

### Finalise

```bash
apk -U upgrade
apk add mkinitfs # update to inital ramfs
apk -vv info|sort # list of installed packages, look for dropbear
apk cache -v sync # download and clean out cache
lbu ci -d
# upgrade instructions here https://wiki.alpinelinux.org/wiki/Upgrading_Alpine
```

## Links

* [XFCE Setup](https://wiki.alpinelinux.org/wiki/XFCE_Setup)
* [Enable Community Repository](https://wiki.alpinelinux.org/wiki/Enable_Community_Repository)
<!-- markdownlint-disable MD034 -->
https://serverfault.com/a/821235
<!-- markdownlint-enable MD034 -->

### Make your own ISO

[How to make a custom ISO image with mkimage](https://wiki.alpinelinux.org/wiki/How_to_make_a_custom_ISO_image_with_mkimage) - note that the architecture has to be the same as the host.

```bash
apk add alpine-sdk build-base apk-tools alpine-conf busybox fakeroot xorriso squashfs-tools sudo mtools dosfstools
adduser build -G abuild
echo "%abuild ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/abuild
abuild-keygen -i -a
git clone https://gitlab.alpinelinux.org/alpine/aports.git
sudo apk update
export PROFILENAME=minimal

cat << EOF > ~/aports/scripts/mkimg.$PROFILENAME.sh
profile_$PROFILENAME() {
        profile_standard
        kernel_cmdline="unionfs_size=512M console=tty0 console=ttyS0,115200"
        syslinux_serial="0 115200"
        kernel_addons=""
        apks="\$apks mdadm mkinitfs mtools rsync sfdisk 
                util-linux dosfstools ntfs-3g"
        local _k _a
        for _k in \$kernel_flavors; do
                apks="\$apks linux-\$_k"
                for _a in \$kernel_addons; do
                        apks="\$apks \$_a-\$_k"
                done
        done
        apks="\$apks linux-firmware"
}
EOF

cd ~/aports/scripts
chmod +x mkimg.$PROFILENAME.sh
mkdir -p ~/iso

sh mkimage.sh --tag edge \
  --outdir ~/iso \
  --arch armv7 \
  --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
  --profile $PROFILENAME
```

[Pro Terminal Commands: Using diskutil](https://applegazette.com/mac/pro-terminal-commands-using-diskutil/)

```mac
diskutil listFilesystems
diskutil list
diskutil eraseDisk MS-DOS ALPINE disk§
diskutil partitionDisk disk§ 2 MBR MS-DOS ALPINE 512MB MS-DOS DATA R
```

Remount media as writeable

```bash
mount /media/mmcblk0p1 -o rw,remount
```

Notes about apk cache [Alpine local backup](https://wiki.alpinelinux.org/wiki/Alpine_local_backup)

<!-- markdownlint-disable MD034 -->
https://github.com/davidmytton/alpine-linux-headless-raspberrypi/releases/download/2021.06.23/headless.apkovl.tar.gz

https://github.com/davidmytton/alpine-linux-headless-raspberrypi
<!-- markdownlint-enable MD034 -->

[Back Up a Flash Memory Installation](https://wiki.alpinelinux.org/wiki/Back_Up_a_Flash_Memory_Installation)
[Manually editing a existing apkovl](https://wiki.alpinelinux.org/wiki/Manually_editing_a_existing_apkovl)
[Local APK cache](https://wiki.alpinelinux.org/wiki/Local_APK_cache)
[Alpine Source Map by boot sequence](https://wiki.alpinelinux.org/wiki/Alpine_Source_Map_by_boot_sequence)

[Alpine Linux APK off-line overlay builder](https://github.com/rnalrd/apkovl-builder/blob/master/create_apkovl.sh)
[Automated provisioning using apkovl](https://blog.w1r3.net/2018/04/16/automated-provisioning-using-apkovl.html)
[Raspberry Pi - Headless Installation](https://wiki.alpinelinux.org/wiki/Raspberry_Pi_-_Headless_Installation)
[Create a bootable SDHC from a Mac](https://wiki.alpinelinux.org/wiki/Create_a_bootable_SDHC_from_a_Mac)

[Raspberry Pi](https://wiki.alpinelinux.org/wiki/Raspberry_Pi)
[Pithy Raspberry Pi installation instructions - including overlay files](https://wiki.alpinelinux.org/wiki/Classic_install_or_sys_mode_on_Raspberry_Pi)

[Semi-Automatic Installation](https://docs.alpinelinux.org/user-handbook/0.1a/Installing/manual.html#_repositories)
[Alpine Linux Install](https://wiki.alpinelinux.org/wiki/Installation)
[How to make a custom ISO image with mkimage](https://wiki.alpinelinux.org/wiki/How_to_make_a_custom_ISO_image_with_mkimage)
[Directly booting an ISO file](https://wiki.alpinelinux.org/wiki/Directly_booting_an_ISO_file)
[QEMU](https://wiki.alpinelinux.org/wiki/Qemu)
[10 Alpine Linux apk Command Examples](https://www.cyberciti.biz/faq/10-alpine-linux-apk-command-examples/)
[How to get regular stuff working](https://wiki.alpinelinux.org/wiki/How_to_get_regular_stuff_working)

[Debugging the Alpine boot process on a Raspberry Pi](https://pi3g.com/2019/01/22/debugging-the-alpine-boot-process/)
[xorg, dwm](https://wiki.alpinelinux.org/wiki/Dwm#Installing_Xorg)
