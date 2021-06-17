---
date: "2021-06-17"
title: "Arch Linux Installation"
---

<!-- markdownlint-disable MD025 -->
# Arch Linux Installation
<!-- markdownlint-enable MD025 -->

## Introduction

My pithy guide to setup Arch Linux. The official Arch installation instructions are on the [Wiki](https://wiki.archlinux.org/index.php/Installation_guide).

## Booting

Boot from a USB media or run `pacman -S arch-install-scripts` to get the standard Linux installation scripts.

```bash
timedatectl set-ntp true
```

## Disk sizing and setup

Get the block size of disks `blockdev --getsz /dev/sda` the smallest 2GB SD card that I own has 3840000 512 byte blocks.

To get progress of `sync` run `watch -d grep -e Dirty: -e Writeback: /proc/meminfo`

I use a single disk for the whole operating system and a 1GB partition at the beginning of the disk as the EFI partition. In my view, operating systems should be disposable, so the more self-contained they are the better. Data, and  possibly user settings, should be very carefully looked after. I avoid using any swapfiles by installing lots of RAM in the first place and building a minimal system.

## pacstrap

Mount the correct drives and install a minimal system. Enough to chroot and setup pacman properly.

```bash
mount /dev/sda2 /mnt # substitute /dev/sda2 as needed
dhcpcd # ethernet
pacstrap /mnt base linux linux-firmware vi # vi for editing, plus any other required pacmages to get started
genfstab -U /mnt >> /mnt/etc/fstab # for the fstab.  Don't add EFI so that it's harder for the operating system to muck about with it
mkdir /mnt/boot/efi # needed for EFI
mount /dev/sda1 /mnt/boot/efi # so that we can do EFI partition stuff later
arch-chroot /mnt
```

## Language

Needs to be moved to after booting for the first time

```bash
vi /etc/locale.gen
# uncomment the line "en_GB.UTF-8 UTF-8"
locale-gen
localectl set-locale LANG=en_GB.UTF-8
localectl set-keymap uk
localectl # check
```

## Adjust pacman to run faster

```bash
pacman -S reflector rsync curl
cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.bak # just in case
reflector --verbose --country 'United Kingdom' -l 10 --sort rate --save /etc/pacman.d/mirrorlist
```

Arch comes with almost nothing by default.

```bash
pacman -S unzip sudo nano vim dhcpcd efibootmgr openssh git ntp
```

* unzip - unziping EFI Shell and rEFInd
* sudo - run commands as superuser
* nano - minimal visual editor
* vim - keystroke driven editor
* dhcpcd - request IP address from servers
* efibootmgr - manage system boot
* openssh - allow ssh into this machine
* git - for software management
* ntp - syncronise time

## Users  

Change root password, create a new user and add it to the appropriate groups.

```bash
passwd # for root
useradd -m -G wheel,audio,uucp jack -s /bin/bash
passwd jack
visudo # uncomment "%wheel ALL=(ALL) NOPASSWD: ALL"
su jack
cd
pwd # should be /home/jack
git clone https://github.com/jchidley/jchidley.github.io.git # instructions
exit # back to root
```

## Minimal Setup

```bash
localectl # check language
systemctl enable dhcpcd.service # so that we have networking on restart
ln -sf /usr/share/zoneinfo/Europe/London /etc/localtime
hwclock --systohc
vi /etc/hostname # add hostname
systemctl enable sshd
```

[Language settings](https://wiki.archlinux.org/index.php/Localewif)

## Boot

Getting the thing to boot the raw EFI way.

```bash
pacman -S intel-ucode
mkdir /boot/efi/nuc3arch1 # In the EFI boot partition
rsync /boot/* /boot/efi/nuc3arch1/ # copy all of the boot files across
```

Create an EFI shell script to boot the new opearting system.

Tabbing for completion speeds this up and avoids errors

```bash
ls /boot/efi/nuc3arch1 > nuc3arch1.nsh
ls /boot/efi/vmlinuz-linux >> nuc3arch1.nsh
lsblk -o NAME,UUID | grep sda2 >> /boot/efi/nuc3arch1.nsh # assuming /dev/sda2 is operating system partition
ls /boot/efi/intel-ucode.img >> nuc3arch1.nsh
ls /boot/efi/initramfs-linux.img >> nuc3arch1.nsh
vi /boot/efi/nuc3arch1.nsh
```

contents of /boot/efi/nuc3arch1.nsh

```bash
cd nuc3arch1
vmlinuz-linux root=UUID=761edd1d-27d0-406a-8033-45c5654dcbc9 rw initrd=/nuc3arch1/intel-ucode.img initrd=/nuc3arch1/initramfs-linux.img
```

Only need to do this if you're direct booting Arch, otherwise do the EFI shell/rEFInd process.

```bash
lsblk -o NAME,UUID # use the right UUID below
efibootmgr --disk /dev/sda --part 1 --create --label "nuc3arch1" --loader /nuc3arch1/vmlinuz-linux --unicode 'root=UUID=761edd1d-27d0-406a-8033-45c5654dcbc9 rw initrd=/nuc3arch1/intel-ucode.img initrd=/nuc3arch1/initramfs-linux.img' --verbose
efibootmgr -v # check to see what number it is, say 0004
efibootmgr -n 4 # try the next boot without commiting to it
```

If it boots correctly, then...

```bash
efibootmgr -o 4,1,2 # reorder the boot once it has worked
```

As a fail safe, can create a `startup.nsh` file containing this single long line

```bash
\vmlinuz-linux root=/dev/sda2 rw initrd=\initramfs-linux.img
```



## GUI

See 2021-06-15-Arch-Linux-GUI-VNC

## Extras

Create a Python environment `python3 -m venv ~/basic-env` and enable it `source ~/basic-env/bin/activate`
Visual Studio Code (AUR), Gitlens, markdownlint, python, Git History
[Anaconda](https://www.anaconda.com/)
nMigen

## bash config

Things to add to `~/.bash_profile`, which ones on first login:

```bash
tbsm # needs to be last
```

`~/.bashrc` which runs on every interactive shell

```bash
source ~/basic-env/bin/activate # enable a default Python environment to avoid polluting everything
```

## Installed Packages

[pacman/Tips and tricks](https://wiki.archlinux.org/index.php/Pacman/Tips_and_tricks)

Remove orphans

```bash
pacman -Qtdq | pacman -Rns - # remove orphans
pacman -S pacman-contrib # paccache
paccache -rk1 -ruk0 # clean the cache
```

List explicitly installed packages not in the base meta package, base-devel package groups:

```bash
expac -H M "%011m\t%-20n\t%10d" $(comm -23 <(pacman -Qqen | sort) <({ pacman -Qqg base-devel; expac -l '\n' '%E' base; cat pacman_install.txt;} | sort | uniq)) | sort -n
```

```bash
cat << EOF > pacman_install.txt
arch-install-scripts
base
curl
firefox
git
intel-ucode
libftdi
linux
linux-firmware
nano
ntfs-3g
ntp
nvidia-390xx
openssh
python-pip
reflector
rsync
sudo
unzip
usbutils
vi
visual-studio-code-bin
wget
xf86-video-intel
EOF
```

`cat pacman_install.txt | sort | uniq`

## Links

* [Arch Installation](https://wiki.archlinux.org/index.php/Install_Arch_Linux_from_existing_Linux)
"Method B: Using the LiveCD image" files [here](https://mirror.bytemark.co.uk/archlinux/iso/2020.01.01/arch/x86_64/), for example
* [Intel Graphics](https://wiki.archlinux.org/index.php/intel_graphics)
* [AUR - Arch User Repository](https://wiki.archlinux.org/index.php/Arch_User_Repository)
* [Symbol fonts for linux terminals](https://c42f.github.io/2015/12/29/crisp-terminal-fonts.html)
* [Fonts - Arch Linux](https://wiki.archlinux.org/index.php/Fonts#Font_packages)
* [Pacman Tip and Tricks](https://wiki.archlinux.org/index.php/Pacman/Tips_and_tricks)
* [Unified Extensible Firmware Interface](https://wiki.archlinux.org/index.php/Unified_Extensible_Firmware_Interface#UEFI_variables)
