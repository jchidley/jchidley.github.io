---
date: "2020-01-15"
title: "Arch Linux Installation"
---

<!-- markdownlint-disable MD025 -->
# Arch Linux Installation
<!-- markdownlint-enable MD025 -->

## Introduction

A set of instructions to get up and running with Arch Linux.

Arch installation instructions are on the [Wiki](https://wiki.archlinux.org/index.php/Installation_guide).  This is my pithy guide to how I do it.

## Booting

Either boot from a USB media or run `pacman -S arch-install-scripts` (or similar) to get the standard installation scripts from a running Linux system.

```bash
timedatectl set-ntp true
```

## Disk sizing and setup

To get the block size of disks `blockdev --getsz /dev/sda`

Smallest 2GB SD Card that I own: `3840000` 512 byte blocks

To get progress of `sync` run `watch -d grep -e Dirty: -e Writeback: /proc/meminfo`

setup disks - I use a single disk for the whole operating system and a 1GB partition at the beginning of the desk as the EFI partition.  In my view, operating systems should be disposable, so the more self contained they are the better.  Data, and  possibly user settings, should be very carefully looked after.  I try to avoid using any swapfiles by installing lots of RAM in the first place and building a minimal system.

## pacstrap

Mount the correct drives and install a minimal system.  Enough to chroot and setup pacman properly.

```bash
mount /dev/sda2 /mnt # substitute /dev/sda2 as needed
dhcpcd # ethernet
pacstrap /mnt base linux linux-firmware # plus any other required pacmages to get started
genfstab -U /mnt >> /mnt/etc/fstab # for the fstab.  Don't add EFI so that it's harder for the operating system to muck about with it
mkdir /mnt/boot/efi # needed for EFI
mount /dev/sda1 /mnt/boot/efi # so that we can do EFI partition stuff later
arch-chroot /mnt
```

## Adjust pacman to run faster

```bash
pacman -S reflector rsync curl
cp /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.bak # just in case
reflector --verbose --country 'United Kingdom' -l 10 --sort rate --save /etc/pacman.d/mirrorlist
```

Arch comes with almost nothing by default.

```bash
pacman -S unzip # for unziping EFI Shell and rEFInd
pacman -S sudo nano vi vim dhcpcd efibootmgr openssh tmux git # basic utilties
```

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
systemctl enable dhcpcd.service # so that we have networking on restart
ln -sf /usr/share/zoneinfo/Europe/London /etc/localtime
hwclock --systohc
vi /etc/locale.gen
# uncomment the line "en_GB.UTF-8 UTF-8"
locale-gen
localectl set-locale LANG=en_GB.UTF-8
vi /etc/vconsole.conf
# add this line "KEYMAP=uk"
vi /etc/hostname # add hostname
systemctl enable sshd
```

[Language settings](https://wiki.archlinux.org/index.php/Localewif)

## Boot

Getting the thing to boot the raw EFI way.

```bash
pacman -S intel-ucode
mkdir /boot/efi/Arch2Shuttle2 # In the EFI boot partition
rsync /boot/* /boot/efi/Arch2Shuttle2/ # copy all of the boot files across
```

Create an EFI shell script to boot the new opearting system.

Tabbing for completion speeds this up and avoids errors

```bash
ls /boot/efi/Arch2Shuttle2 > Arch2Shuttle2.nsh
ls /boot/efi/vmlinuz-linux >> Arch2Shuttle2.nsh
lsblk -o NAME,UUID | grep sda2 >> /boot/efi/Arch2Shuttle2.nsh # assuming /dev/sda2 is operating system partition
ls /boot/efi/intel-ucode.img >> Arch2Shuttle2.nsh
ls /boot/efi/initramfs-linux.img >> Arch2Shuttle2.nsh
vi /boot/efi/Arch2Shuttle2.nsh
```

contents of /boot/efi/Arch2Shuttle2.nsh

```bash
cd Arch2Shuttle2
vmlinuz-linux root=UUID=23aff7da-45d6-492d-9f9c-b71b531cebfb rw initrd=/Arch2Shuttle2/intel-ucode.img initrd=/Arch2Shuttle2/initramfs-linux.img
```

Only need to do this if you're direct booting Arch, otherwise do the EFI shell/rEFInd process.

```bash
lsblk -o NAME,UUID # use the right UUID below
efibootmgr --disk /dev/sda --part 1 --create --label "Arch 5" --loader /Arch5/vmlinuz-linux --unicode 'root=UUID=23aff7da-45d6-492d-9f9c-b71b531cebfb rw initrd=/Arch5/intel-ucode.img initrd=/Arch5/initramfs-linux.img' --verbose
efibootmgr -v # check to see what number it is, say 0004
efibootmgr -n 4 # try the next boot without commiting to it
```\\e boot once it has worked
```

As a fail safe, can create a ```startup.nsh``` file containing this single long line

```bash
\vmlinuz-linux root=/dev/sda2 rw initrd=\initramfs-linux.img
```

## GUI

```bash
pacman -S xorg-server xfce4
pacman -S xf86-video-intel # card specific video drivers
pacman -S nvidia-390xx # legacy driver front room
```

If you don't load the correct drivers, you get an unhelpful set of errors including ```xinit: unable to connect to X server: Connection refused```.
[Intel Graphics](https://wiki.archlinux.org/index.php/intel_graphics)

Minimal display manager [tbsm](https://aur.archlinux.org/packages/tbsm/) from the [AUR](https://wiki.archlinux.org/index.php/Arch_User_Repository).

```bash
pacman -S base-devel git # for AUR installation
git clone https://aur.archlinux.org/tbsm.git
cd tbsm
makepkg -si # as a normal user
```

Run the display manager and pick the display environment.

```bash
tbsm
pacman -S firefox # web browser
```

## Extras

Visual Studio Code (AUR), Gitlens, markdownlint, python, Git History
[Anaconda](https://www.anaconda.com/)
nMigen

## Installed Packages

[pacman/Tips and tricks](https://wiki.archlinux.org/index.php/Pacman/Tips_and_tricks)

List explicitly installed packages not in the base meta package, base-devel, qt5, xfce4 package groups:

```bash
pacman -S expac
comm -23 <(pacman -Qeq | sort) <({ pacman -Qqg base-devel qt5 xfce4; expac -l '\n' '%E' base; cat pacman_install.txt; } | sort | uniq)
```

```bash
cat << EOF > pacman_install.txt
arch-install-scripts
base
curl
dhcpcd
dosfstools
efibootmgr
eigen
expac
firefox
git
intel-ucode
libftdi
linux
linux-firmware
nano
ntfs-3g
nvidia-390xx
openssh
python-pip
reflector
rsync
sudo
tbsm
tmux
unzip
usbutils
vi
vim
visual-studio-code-bin
wget
xf86-video-intel
xorg-server
zip
EOF
```

`cat pacman_install.txt | sort | uniq`

### tmux commands

Command | output
--- | ---a
[Arch Installation](https://wiki.archlinux.org/index.php/Install_Arch_Linux_from_existing_Linux)
"Method B: Using the LiveCD image" files [here](https://mirror.bytemark.co.uk/archlinux/iso/2020.01.01/arch/x86_64/), for example
[Arch Linux Instllation](https://wiki.archlinux.org/index.php/Installation_guide)
[Intel Graphics](https://wiki.archlinux.org/index.php/intel_graphics)
[tbsm](https://aur.archlinux.org/packages/tbsm/)
[AUR](https://wiki.archlinux.org/index.php/Arch_User_Repository).
