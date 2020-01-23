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

This command ```pacman -S arch-install-scripts``` will allow you run the standard installation scripts from a running Arch system.  May be availble from other distributions too.

To get an ordered list of the fastest responding repositories:

````bash
sudo pacman -S reflector rsync curl
sudo cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.bak # just in case
sudo reflector --verbose --country 'United Kingdom' -l 5 --sort rate --save /etc/pacman.d/mirrorlist
````

Some basic utilties.  Arch comes with almost nothing by default.

````bash
pacman -S sudo nano vi dhcpcd efibootmgr openssh
````

User management.  Change root password, create a new user and add it to the appropriate groups.

````bash
passwd # for root
useradd -m -G wheel,audio jack -s /bin/bash
passwd jack
#using the command below, uncomment "%wheel ALL=(ALL) NOPASSWD: ALL" line
EDITOR=nano visudo
````

Getting the thing to boot the raw EFI way.

````bash
pacman -S intel-ucode
mkdir /Arch5 # In the EFI boot partition
cp /boot/* /Arch5/* # copy all of the boot files across
lsblk -o NAME,UUID # use the right UUID below
efibootmgr --disk /dev/sda --part 1 --create --label "Arch 5" --loader /Arch5/vmlinuz-linux --unicode 'root=UUID=23aff7da-45d6-492d-9f9c-b71b531cebfb rw initrd=/Arch5/intel-ucode.img initrd=/Arch5/initramfs-linux.img' --verbose
efibootmgr -v # check to see what number it is, say 0004
efibootmgr -n 4 # try the next boot without commiting to it
````

If it boots correctly, then...

````bash
efibootmgr -o 4,1,2 # reorder the boot once it has worked
````

As a fail safe, can create a ```startup.nsh``` file containing this single long line

````bash
\vmlinuz-linux root=/dev/sda2 rw initrd=\initramfs-linux.img
````

Edit the system's name in ```/etc/hostname```

[Language settings](https://wiki.archlinux.org/index.php/Localewif)

````bash
vi /etc/locale.gen
# uncomment the line "en_GB.UTF-8 UTF-8"
locale-gen
localectl set-locale LANG=en_GB.UTF-8
vi /etc/vconsole.conf
# add this line "KEYMAP=uk"
````

Get networking started and add the ssh daemon so that we can log in remotely.

````bash
systemctl enable dhcpcd.service
systemctl start dhcpcd.service
pacman -S openssh
systemctl enable sshd
systemctl start sshd
````

GUI

````bash
pacman -S xorg-server xfce4
pacman -S xf86-video-intel # card specific video drivers
````

If you don't load the correct drivers, you get an unhelpful set of errors including ```xinit: unable to connect to X server: Connection refused```.
[Intel Graphics](https://wiki.archlinux.org/index.php/intel_graphics)

Minimal display manager [tbsm](https://aur.archlinux.org/packages/tbsm/) from the AUR.  AUR installation instructions [here](https://wiki.archlinux.org/index.php/Arch_User_Repository).

````bash
pacman -S base-devel # for AUR installation
git clone https://aur.archlinux.org/tbsm.git
cd tbsm
makepkg -si # as a normal user
````

Run the display manager and pick the display environment.

````bash
tbsm
````

Web browser

````bash
pacman -S firefox
````

## Links

* [Arch Installation](https://wiki.archlinux.org/index.php/Install_Arch_Linux_from_existing_Linux)
"Method B: Using the LiveCD image" files [here](https://mirror.bytemark.co.uk/archlinux/iso/2020.01.01/arch/x86_64/), for example
* [Arch Linux Instllation](https://wiki.archlinux.org/index.php/Installation_guide)
