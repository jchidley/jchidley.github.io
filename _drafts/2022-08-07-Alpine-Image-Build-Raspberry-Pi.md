---
---

<!-- markdownlint-disable MD025 -->
# Alpine Image Build Raspberry Pi
<!-- markdownlint-enable MD025 -->

## Introduction

What makes [Alpine Linux](https://alpinelinux.org/about/) interesting? It is an extremely lightweight and easy to configure system. To really appreaciate just what it offers an administrator look at [these system backup instructions](https://wiki.alpinelinux.org/wiki/Back_Up_a_Flash_Memory_Installation). To build a new system, based on an existing one, take a backup (or use a vanilla [installation file](https://alpinelinux.org/downloads/)), edit or write [the configuration file - AKA apkvol](https://wiki.alpinelinux.org/wiki/Manually_editing_a_existing_apkovl) and add the necessary packages to both [the local cache](https://wiki.alpinelinux.org/wiki/Local_APK_cache) and the `/etc/apk/world` file. `lbu commit` and you are done.

[This guide](https://wiki.alpinelinux.org/wiki/Alpine_Source_Map_by_boot_sequence) describes how Alpine Linux boots and there's a [detailed version for the Raspberry Pi](https://pi3g.com/2019/01/10/alpine-boot-process-on-the-raspberry-pi/). Finally, if you're missing a favourite command then `akp search [faviourite missing command]` is what you need before you `apk add [found package name]`.

For more detailed information see the [Alpine User Handbook](https://docs.alpinelinux.org/user-handbook/0.1a/index.html) and the [Developer Documentation](https://wiki.alpinelinux.org/wiki/Category_talk:Developer_Documentation).

This is the Linux that I have been waiting for.

### On the Build machine

This should probably be done in a `chroot` [Alpine Linux in a chroot - Alpine Linux](https://wiki.alpinelinux.org/wiki/Alpine_Linux_in_a_chroot#Install_the_alpine_base_installation_onto_the_chroot)

```bash 
mirror='http://dl-cdn.alpinelinux.org/alpine/'
arch='aarch64'
version='2.12.9-r3'
curl -LO ${mirror}/latest-stable/main/${arch}/apk-tools-static-${version}.apk
```
[GitHub - alpinelinux/alpine-chroot-install: Install Alpine Linux in chroot with a breeze. Build ARM on Travis CI or any other x86_64 CI.](https://github.com/alpinelinux/alpine-chroot-install/)

[Install Alpine on a Raspberry Pi](https://wiki.alpinelinux.org/wiki/Raspberry_Pi)

We're going to install Alpine in "diskless" mode and use overlay files. Prepare an SD card with 500MB DOS bootable partition with the remainder as ext4
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

[downloads | Alpine Linux](https://alpinelinux.org/downloads/)

[Select - yq](https://mikefarah.gitbook.io/yq/operators/select)

```bash
mkfs.fat ${PIDEVICE}1
mkfs.ext2 ${PIDEVICE}2 # unnecessary
# https://alpinelinux.org/downloads/
# armv7 works on every Pi except the first Model A and Model B
cd ~/Downloads # or /home/username/Downloads
apk add yq
arm7release='https://dl-cdn.alpinelinux.org/alpine/latest-stable/releases/armv7/'
wget "$arm7release/latest-releases.yaml" -O latest-releases.yaml 
alpine_file=$(yq '.[] | select(.title == "*Raspberry*Pi*")'.file latest-releases.yaml)
wget "$arm7release/$alpine_file" -O $alpine_file
check=$(yq '.[] | select(.title == "*Raspberry*Pi*")'.sha256 latest-releases.yaml)
# Two spaces between https://stackoverflow.com/a/37499133/3617057
echo "$check  $alpine_file" | sha256sum -c -
tdrive="$(mktemp -d /tmp/alpine_install.XXXXXX)"
mount ${PIDEVICE}1 $tdrive
tar -xvf $alpine_file -C $tdrive --no-same-owner
sync
```

<!-- unconfirmed extra bits -->
USB network

```bash
sudo tee -a $tdrive/usercfg.txt > /dev/null << "EOF"
dtoverlay=dwc2,dr_mode=peripheral
EOF
```

```bash
setup-sshd
modprobe dwc2
modprobe g_ether
ip link set usb0 up
ip addr add 192.168.101.101/16 dev usb0
ping 192.168.101.102 # iPad
apk add openssh
echo "root:secret" | chpasswd
cat /etc/apk/world
cat /etc/apk/cache

mount /media/mmcblk0p1 -o rw,remount
```

Not confirmed

```bash
sudo tee -a /mnt/sdb1/config.txt > /dev/null << "EOF"
dtoverlay=dwc2,dr_mode=peripheral
EOF
sudo sed -i -E -e 's/(^.* )(rootwait.*$)/\1modules-load=dwc2,g_ether \2/' \
    /mnt/sdb1/cmdline.txt
```

temporary bits for testing

```bash
sync # make sure all the files are written to the SD card
umount $tdrive
rmdir $tdrive
```
<!-- unconfirmed extra bits END -->

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

`haveged` competes with the broadcom provided random number generator, now `iproc-rng200` (previously `bcm2835_rng` and `bcm2708-rng`) and so it needs to be disabled

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

* [Enable Community Repository](https://wiki.alpinelinux.org/wiki/Enable_Community_Repository)
* [virtualization - How to zero fill a virtual disk's free space on windows for better compression? - Server Fault](https://serverfault.com/questions/165070/how-to-zero-fill-a-virtual-disks-free-space-on-windows-for-better-compression/821235#821235)

## Make your own Alpine Image

[How to make a custom ISO image with mkimage](https://wiki.alpinelinux.org/wiki/How_to_make_a_custom_ISO_image_with_mkimage) - note that the architecture has to be the same as the host.
Broadcom WiFi and Wireguard, information about ISO customisation[USB Linux - Alpine ISO build](https://jpselby.co.uk/projects/usb-linux-1/)
[How to run an unattended install of Alpine Linux](https://wejn.org/2022/04/alpinelinux-unattended-install/)
[Kloster - Live CD image](https://eyedeekay.github.io/kloster/)

An image build is really three things:
1. Bake an image with everything included for offline use
2. make an apkovl (overlay file) that includes all the required configuration
3. make a script to run on first boot to complete setup (say doing the `apk add` commands)

### Setup for Image Build

```bash
apk add alpine-sdk build-base apk-tools alpine-conf busybox fakeroot xorriso squashfs-tools sudo # removed syslinux
apk add tmux # for ssh from iPad
apk add mkinitfs
echo "%abuild ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/abuild
su - build
abuild-keygen -i -a
git clone --depth=1 https://gitlab.alpinelinux.org/alpine/aports.git
```

```ash
cat > pibuild <<\EOF
sh aports/scripts/mkimage.sh --tag edge \
--repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
--arch armv7 \
--outdir ~/iso \
--profile $1 \
$2
#pibuild rpi --simulate
EOF
chmod +x pibuild
```

### Image build

```ash
# mv aports/scripts/mkimg.arm.sh aports/scripts/bak.mkimg.arm.sh
cp aports/scripts/bak.mkimg.arm.sh aports/scripts/mkimg.arm.sh
# get rid of uboot stuff
sed -i '/build_uboot/,$ d' aports/scripts/mkimg.arm.sh
```

```ash
~/pibuild rpi
# test for config and cmdline as these things disappear
tar tf iso/alpine-rpi-edge-armv7.tar.gz | sed -n -e '/config.txt/ p' -e '/cmdline.txt/ p'
```

remove the various architecture options
```ash
sed -i -r '/kernel_flavors="rpi"/,/easc/ {
s/(kernel_flavors="rpi)(")/\12\"/
/case "\$ARCH"/,/esac/ d
}' aports/scripts/mkimg.arm.sh
```

combinged with above, limit the build to just rpi2
```ash
sed -i -r 's/(kernel_flavors="rpi)(")/\12/' aports/scripts/mkimg.arm.sh
```

add the broadcom firmware, for WiFi
```ash
sed -i '/kernel_flavors="rpi2"/ a\
\tapks="\$apks linux-firmware-brcm"' \
aports/scripts/mkimg.arm.sh
```

add apkvol
```ash
sed -i '/kernel_flavors="rpi2"/ a\
\tapkovl="genapkovl-dhcp.sh"' \
aports/scripts/mkimg.arm.sh
```

keep only the top, generic rpi, stuff. This also remove the uboot stuff
```bash
cp aports/scripts/bak.mkimg.arm.sh aports/scripts/mkimg.arm.sh
sed -i '/profile_rpi()/,$ d' aports/scripts/mkimg.arm.sh
```

Full replacement.
genapkovl-chidley.sh needs to match path/filename for the apkovl overlay file, below
```ash
tee -a aports/scripts/mkimg.arm.sh <<\EOF 
profile_rpi() {
        profile_base
        title="Raspberry Pi"
        desc="Includes Raspberry Pi kernel"
        image_ext="tar.gz"
        arch="aarch64 armhf armv7"
        kernel_flavors="rpi2"
        apkovl="genapkovl-chidley.sh"
        apks="$apks linux-firmware-brcm"
        kernel_cmdline="console=tty1 console=serial0,115200"
        initfs_features="base squashfs mmc usb kms dhcp https"
        hostname="rpi"
        grub_mod=
}
EOF
```

```ash
~/pibuild rpi --simulate
```

example output
```ash
OK: 0 MiB in 0 packages
fetch http://dl-cdn.alpinelinux.org/alpine/edge/main/armv7/APKINDEX.tar.gz
v20220809-216-g7a8e9f1179 [http://dl-cdn.alpinelinux.org/alpine/edge/main]
OK: 4945 distinct packages available
>>> mkimage-armv7: Building rpi
>>> mkimage-armv7: --> rpi_config 0d85770dcadb24993fb3ca99e72d2c5984f11e54
>>> mkimage-armv7: --> rpi_blobs 
>>> mkimage-armv7: --> kernel armv7 rpi2 f69b20ece0912a894f1af72f607f213090d3ffd4 linux-rpi2 linux-firmware wireless-regdb
>>> mkimage-armv7: --> apks armv7 76f3a1bd1f8a9fbfde581a87139bb0262dc16806
>>> mkimage-armv7: --> apkovl rpi 45c666005250fdd2ba8fa97e79a9d8fc40f2cb55
>>> mkimage-armv7: Creating alpine-rpi-edge-armv7.tar.gz
Images generated in /home/build/iso
```

### Make an apkovl Overaly File

```ash
cat > genapkovl-chidley.sh <<\EOFgenapkovl
#!/bin/sh -e

HOSTNAME="$1"
if [ -z "$HOSTNAME" ]; then
	echo "usage: $0 hostname"
	exit 1
fi

cleanup() {
	rm -rf "$tmp"
}

makefile() {
	OWNER="$1"
	PERMS="$2"
	FILENAME="$3"
	cat > "$FILENAME"
	chown "$OWNER" "$FILENAME"
	chmod "$PERMS" "$FILENAME"
}

rc_add() {
	mkdir -p "$tmp"/etc/runlevels/"$2"
	ln -sf /etc/init.d/"$1" "$tmp"/etc/runlevels/"$2"/"$1"
}

tmp="$(mktemp -d)"
trap cleanup EXIT

mkdir -p "$tmp"/etc
makefile root:root 0644 "$tmp"/etc/hostname <<EOF
$HOSTNAME
EOF

mkdir -p "$tmp"/etc/network
makefile root:root 0644 "$tmp"/etc/network/interfaces <<EOF
auto lo
iface lo inet loopback

auto wlan0
iface wlan0 inet dhcp
EOF

mkdir -p "$tmp"/etc/apk
makefile root:root 0644 "$tmp"/etc/apk/world <<EOF
alpine-base
linux-firmware-brcm
wpa_supplicant
EOF

mkdir -p "$tmp"/etc/wpa_supplicant
makefile root:root 0644 "$tmp"/etc/wpa_supplicant/wpa_supplicant.conf << "EOF"                                                   
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

rc_add devfs sysinit
rc_add dmesg sysinit
rc_add mdev sysinit
rc_add hwdrivers sysinit
rc_add modloop sysinit

rc_add hwclock boot
rc_add modules boot
rc_add sysctl boot
rc_add hostname boot
rc_add bootmisc boot
rc_add syslog boot

rc_add networking boot
rc_add wpa_supplicant boot

rc_add mount-ro shutdown
rc_add killprocs shutdown
rc_add savecache shutdown

tar -c -C "$tmp" etc | gzip -9n > $HOSTNAME.apkovl.tar.gz
EOFgenapkovl
```

### First Script

### Copy image to sdcard

```ash
sudo su
PIDEVICE=/dev/sdX
mkfs.fat ${PIDEVICE}1
tdrive="$(mktemp -d /tmp/alpine_install.XXXXXX)"
mount ${PIDEVICE}1 $tdrive
alpine_file=/alpine/home/build/iso/alpine-rpi-edge-armv7.tar.gz
#alpine_file=/alpine/home/build/iso/alpine-jackpi-edge-armv7.tar.gz
tar -xvf $alpine_file -C $tdrive --no-same-owner
# ====== brcm wifi firmware not automatically downloaded
# https://gitlab.alpinelinux.org/alpine/aports/-/issues/13302#note_255137
cd ~
wget https://dl-cdn.alpinelinux.org/alpine/latest-stable/main/armv7/linux-firmware-brcm-20220509-r1.apk 
mkdir -p $tdrive/firmware
# --strip-components=1 removes the top level directory in the archive
tar -xvf ~/linux-firmware-brcm-20220509-r1.apk -C $tdrive --strip-components=1
# ======
tee -a $tdrive/usercfg.txt > /dev/null << "EOF"
enable_uart=1
EOF
sync
umount $tdrive
exit
```

```ash
# from a running Pi
minicom --device /dev/serial0 --baudrate 115200
```

### mac related

[Pro Terminal Commands: Using diskutil](https://applegazette.com/mac/pro-terminal-commands-using-diskutil/)

```mac
diskutil listFilesystems
diskutil list
diskutil eraseDisk MS-DOS ALPINE disk
diskutil partitionDisk disk§ 2 MBR MS-DOS ALPINE 512MB MS-DOS DATA R
```

[Create a bootable SDHC from a Mac](https://wiki.alpinelinux.org/wiki/Create_a_bootable_SDHC_from_a_Mac)

Remount media as writeable

```bash
mount /media/mmcblk0p1 -o rw,remount
```

### Installation

Once you know the source for packages, it should be relatively easy to build a customised image with an overlay file (apkvol). That can contain a startup script (`/etc/local.d/00_first_script.start`) and `/etc/apk/world` for packages to install at boot.

Given a working Alpine image, build a suitable apkvol, downloading required files and customising it [apkovl-builder](https://github.com/rnalrd/apkovl-builder/blob/master/create_apkovl.sh)

Notes about apk cache [Alpine local backup](https://wiki.alpinelinux.org/wiki/Alpine_local_backup)
[Local APK cache](https://wiki.alpinelinux.org/wiki/Local_APK_cache)
[Headless Alpine Linux deployment scripts](https://github.com/macmpi/alpine-linux-headless-bootstrap)

Some hints and tips from various scripts [Pi-Factory](https://pi-factory.readthedocs.io/en/latest/README.html)
General installation stuff [How to Install Alpine Linux on Raspberry Pi](https://www.maxrodrigo.com/posts/how-to-install-alpine-on-raspberry-pi/)
[Back Up a Flash Memory Installation](https://wiki.alpinelinux.org/wiki/Back_Up_a_Flash_Memory_Installation)
[Manually editing a existing apkovl](https://wiki.alpinelinux.org/wiki/Manually_editing_a_existing_apkovl)
[Setting up a SSH server](https://wiki.alpinelinux.org/wiki/Setting_up_a_SSH_server)
[Alpine Linux in a chroot - Alpine Linux](https://wiki.alpinelinux.org/wiki/Alpine_Linux_in_a_chroot#Install_the_alpine_base_installation_onto_the_chroot)

### General Alpine Linux stuff

[paulgorman.org/technical](https://paulgorman.org/technical/linux-alpine.txt.html)
[Alpine Linux on Raspberry Pi: Diskless Mode with persistent storage](https://thiagowfx.github.io/2022/01/alpine-linux-on-raspberry-pi-diskless-mode-with-persistent-storage/)
GUI on a Pi [Tutorial: 64-bit Alpine Linux Desktop on the Raspberry Pi 4](https://www.maxocull.com/2019/12/25/Alpine-Desktop-on-the-Raspberry-Pi-4/)
[Writing Init Scripts - Alpine Linux](https://wiki.alpinelinux.org/wiki/Writing_Init_Scripts)

[`/etc/modules` not used to load modules (#11545) · Issues · alpine / aports · GitLab](https://gitlab.alpinelinux.org/alpine/aports/-/issues/11545)

[Alpine Source Map by boot sequence](https://wiki.alpinelinux.org/wiki/Alpine_Source_Map_by_boot_sequence)

[Raspberry Pi](https://wiki.alpinelinux.org/wiki/Raspberry_Pi)
[Pithy Raspberry Pi installation instructions - including overlay files](https://wiki.alpinelinux.org/wiki/Classic_install_or_sys_mode_on_Raspberry_Pi)

[Semi-Automatic Installation](https://docs.alpinelinux.org/user-handbook/0.1a/Installing/manual.html#_repositories)
[Alpine Linux Install](https://wiki.alpinelinux.org/wiki/Installation)
[Directly booting an ISO file](https://wiki.alpinelinux.org/wiki/Directly_booting_an_ISO_file)
[QEMU](https://wiki.alpinelinux.org/wiki/Qemu)
[10 Alpine Linux apk Command Examples](https://www.cyberciti.biz/faq/10-alpine-linux-apk-command-examples/)

[Alpine boot process on the Raspberry Pi - pi3g.com](https://pi3g.com/2019/01/10/alpine-boot-process-on-the-raspberry-pi/)
[Debugging the Alpine boot process on a Raspberry Pi](https://pi3g.com/2019/01/22/debugging-the-alpine-boot-process/)
