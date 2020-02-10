---
date: "2020-01-15"
title: "Arch Linux Installation"
---

<!-- markdownlint-disable MD025 -->
# Arch Linux Installation
<!-- markdownlint-enable MD025 -->

## Introduction

A set of instructions to get up and running with Arch Linux.

## Booting Sequence

Arch installation instructions are on the [Wiki](https://wiki.archlinux.org/index.php/Installation_guide).  This is my pithy guide to how I do it.

```bash
timedatectl set-ntp true
```

setup disks - I use a single disk for the whole operating system and a 1GB partition at the beginning of the desk as the EFI partition.  In my view, operating systems should be disposable, so the more self contained they are the better.  Data, and  possibly user settings, should be very carefully looked after.  I try to avoid using any swapfiles by installing lots of RAM in the first place.

```bash
mount /dev/sda2 /mnt # substitute /dev/sda2 as needed
pacstrap /mnt base linux linux-firmware # plus any other required pacmages to get started
genfstab -U /mnt >> /mnt/etc/fstab # for the fstab.  Don't add EFI so that it's harder for the operating system to muck about with it
mkdir /mnt/boot/efi # needed for EFI
mount /dev/sda1 /mnt/boot/efi # so that we can do EFI partition stuff later
arch-chroot /mnt
```

This command ```pacman -S arch-install-scripts``` will allow you run the standard installation scripts from a running Arch system.  May be availble from other distributions too.

To get an ordered list of the fastest responding repositories:

```bash
pacman -S reflector rsync curl
cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.bak # just in case
reflector --verbose --country 'United Kingdom' -l 10 --sort rate --save /etc/pacman.d/mirrorlist
```

Arch comes with almost nothing by default.

```bash
pacsman -S unzip # for unziping EFI Shell and rEFInd
pacman -S sudo nano vim dhcpcd efibootmgr openssh tmux git # basic utilties
```

User management.  Change root password, create a new user and add it to the appropriate groups.

```bash
passwd # for root
useradd -m -G wheel,audio jack -s /bin/bash
passwd jack
visudo # uncomment "%wheel ALL=(ALL) NOPASSWD: ALL"
```

```bash
su jack
cd /home/jack
git clone https://github.com/jchidley/jchidley.github.io.git # instructions
exit
tmux # to split windows and copy **stuff**
```

### tmux commands

Command | output
--- | ---
Ctrl-b % | new window
Ctrl-arrow keys | move between windows
Ctrl-b [ | copy stuff
Ctrl-space | begin mark
Ctrl-w | end mark/copy command
Ctrl-b ] | paste



```bash
systemctl enable dhcpcd.service # so that we have networking on restart
ln -sf /usr/share/zoneinfo/Europe/London /etc/localtime #not working?
hwclock --systohc
vi /etc/locale.gen # Uncomment en_GB.UTF-8 & en_US.UTF-8
locale-gen
vi /etc/locale.conf # LANG=en_GB.UTF-8
vi /etc/hostname # add hostname
# mkinitcpio -P # usually already done as part of pacstrap
```

Getting the thing to boot the raw EFI way.

```bash
pacman -S intel-ucode
mkdir /boot/efi/Arch2Shuttle2 # In the EFI boot partition
cp /boot/* /boot/efi/Arch2Shuttle2/* # copy all of the boot files across
```

Create an EFI shell script to boot the new opearting system.

```bash
lsblk -o NAME,UUID | grep /dev/sda2 >> /boot/efi/Arch2Shuttle2.nsh # assuming /dev/sda2 is operating system partition
vi /boot/efi/Arch2Shuttle2.nsh
```

FS0: is the first disk as the firmware detects and orders them.

contents of /boot/efi/Arch2Shuttle2.nsh

```bash
FS0:
cd Arch2Shuttle2
vmlinuz-linux root=UUID=23aff7da-45d6-492d-9f9c-b71b531cebfb rw initrd=/Arch2Shuttle2/intel-ucode.img initrd=/Arch2Shuttle2/initramfs-linux.img
```

Only need to do this if you're direct booting Arch, otherwise do the EFI shell/rEFInd process.

```bash
lsblk -o NAME,UUID # use the right UUID below
efibootmgr --disk /dev/sda --part 1 --create --label "Arch 5" --loader /Arch5/vmlinuz-linux --unicode 'root=UUID=23aff7da-45d6-492d-9f9c-b71b531cebfb rw initrd=/Arch5/intel-ucode.img initrd=/Arch5/initramfs-linux.img' --verbose
efibootmgr -v # check to see what number it is, say 0004
efibootmgr -n 4 # try the next boot without commiting to it
```

If it boots correctly, then...

```bash
efibootmgr -o 4,1,2 # reorder the boot once it has worked
```

As a fail safe, can create a ```startup.nsh``` file containing this single long line

```bash
\vmlinuz-linux root=/dev/sda2 rw initrd=\initramfs-linux.img
```

Edit the system's name in ```/etc/hostname```

[Language settings](https://wiki.archlinux.org/index.php/Localewif)

```bash
vi /etc/locale.gen
# uncomment the line "en_GB.UTF-8 UTF-8"
locale-gen
localectl set-locale LANG=en_GB.UTF-8
vi /etc/vconsole.conf
# add this line "KEYMAP=uk"
```

Get networking started and add the ssh daemon so that we can log in remotely.

```bash
systemctl enable dhcpcd.service
systemctl start dhcpcd.service
pacman -S openssh
systemctl enable sshd
systemctl start sshd
````

GUI

```bash
pacman -S xorg-server xfce4
pacman -S xf86-video-intel # card specific video drivers
pacman -S nvidia-390xx # legacy driver front room
```

If you don't load the correct drivers, you get an unhelpful set of errors including ```xinit: unable to connect to X server: Connection refused```.
[Intel Graphics](https://wiki.archlinux.org/index.php/intel_graphics)

Minimal display manager [tbsm](https://aur.archlinux.org/packages/tbsm/) from the AUR.  AUR installation instructions [here](https://wiki.archlinux.org/index.php/Arch_User_Repository).

```bash
pacman -S base-devel git # for AUR installation
git clone https://aur.archlinux.org/tbsm.git
cd tbsm
makepkg -si # as a normal user
```

Run the display manager and pick the display environment.

```bash
tbsm
```

Web browser

```bash
pacman -S firefox
```

## Links

* [Arch Installation](https://wiki.archlinux.org/index.php/Install_Arch_Linux_from_existing_Linux)
"Method B: Using the LiveCD image" files [here](https://mirror.bytemark.co.uk/archlinux/iso/2020.01.01/arch/x86_64/), for example
* [Arch Linux Instllation](https://wiki.archlinux.org/index.php/Installation_guide)
