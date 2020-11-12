---
date: "2020-01-15"
title: "Booting Linux and Operating System Choice"
---

<!-- markdownlint-disable MD025 -->
# Booting Linux and Operating System Choice
<!-- markdownlint-enable MD025 -->

## Introduction

I want to install multiple operating systems on my computer and choose which one to boot with the minimum amount of fuss.  I had thought that this was a solved problem.  How wrong I was.

I have converted my computers, even the old ones, to UEFI to make things consistent.  At a pinch, I can boot MBR disks.  My target operating systems are Linux and Windows.

What I have learned is that booting is it's own process.  It's best to use programs that are designed to run in the UEFI environment directly and not things provided by any operating system.  Every operating system takes booting very seriously and each is liable to make decisions about booting which may interefere with other operating systems' ability to boot.  GRUB for example has it's own boot loader and I've found that Ubuntu's version of GRUB will not boot Arch Linux successfully - giving "Authentication Errors" when I tried to login.

## Booting Sequence

Keeping things simple, I use only UEFI capable hardware.  The proccess is:

1. Hardare boots, checks its boot order list (kept in NVRAM - non-volatile RAM) and runs the first item.  If that doesn't work, it progresses down the list.
1. If it's an EFI bootable operating system, you're done.
1. If it is a "boot manager" - they're generally not good managers - or "boot loader" - ditto - then this runs and gives its choices.  This process repeats until an operating system is booted.

## Perscriptive Advice

The steps below will ensure that the computer will always boot and can resuce mistakes.  It requires manually copying files from each operating system's normal boot localion to the EFI system partition.  A small price to pay for predictability.

1. Boot from a Linux live or installation USB of some sort
1. Create a 1GB EFI system partition formatted to fat32
1. Install the UEFI shell
1. Install rEFInd
1. Create a startup.nsh script that boots rEFInd
1. Set the boot sequence to the shell first, rEFInd second
1. Copy all operating systems boot files into the system partition
1. Create a UEFI script for the operating system and a startup.nsh for rEFInd
1. Make all copies of Windows UEFI bootable (not a simple process)

## Hardare UEFI Configuration

On older systems, the boot order in the BIOS / UEFI might override any settings applied in software.  For the Shuttle boxes that I use, I had to change the boot to "Windows 8.1/10" from "Windows 7" this disabled a lot of boot choices in the firmware settings.

## EFI Operating System Boot

Find and follow the operating system specific way to boot from EFI directly.  This is the fail safe way to do things.  The information for Arch linux is [here](https://wiki.archlinux.org/index.php/EFISTUB).  Windows and Linux have their own utilities for this: efibootmgr and bcdedit.

### efibootmgr (Linux)

Copy all of the required boot files to their own directory, say `Arch5`, in the EFI system drive and create an EFI shell script to boot it.  

To boot this directly from hardware add an entry to the EFI NVRAM like this:

```shell
efibootmgr -v # check the current boot order
efibootmgr --disk /dev/sda --part 1 --create --label "Arch 5" --loader /Arch5/vmlinuz-linux --unicode 'root=UUID=23aff7da-45d6-492d-9f9c-b71b531cebfb rw initrd=/Arch5/initramfs-linux.img' --verbose
efibootmgr -o 0,1 # reset the boot order back to what it was orginally
efibootmgr -n 2 # to run the newly added item at next boot
```

#### EIF Booting Windows (bcdedit)

[MBR2GPT command](https://docs.microsoft.com/en-us/windows/deployment/mbr-to-gpt) to convert system drive to EFI.  Move partition to EFI drives by using DD (Linux) or back tool for Windows.

```shell
bcdedit /v
```

## UEFI Shell

I have found that shells, and other pre-opeating system utilties/enviroments like boot managers, need to be installed from the original sources.  Operating system providers tend to customise these things and hence they don't always work with other operating systems.

[TianoCore](https://www.tianocore.org/) provides "an open source implementation of the Unified Extensible Firmware Interface" and a release can be downloaded [here](https://github.com/tianocore/edk2/releases).  I put mine in the root of the EFI partion in /UefiShell and ran this to add it to NVRAM, same process as to add an operating system, above.

```shell
rsync -r /mnt/ShellBinPkg/UefiShell /boot/efi/
cd /boot/efi
efibootmgr -c -l -v UefiShell/X64/Shell.efi -L "TianoCore UEFI Shell" # works if relative 
efibootmgr --disk /dev/sda --part 1 --create --label "TianoCore UEFI Shell" --loader  --verbose
```

Note: this is a single long line.

Here are some useful EFI commands:
Merge 20200312
1. `help -b` the -b is for output pagination.
1. `mode` to view and change the number of lines and columns displayed.
1. `map` displays some of the devices available.  On my system there's a series of drives labelled `FS0` (for UEFI known file systems), `BLK1` (block devices), etc.
1. `FS0:` to change to a file system.
1. `ls` to list files, directories.  `cd` change directories

To actually boot things requires that:

1. You know the EFI command to run your operating system.  The command needs to be a single line e.g.  
`vmlinuz-linux root=/dev/sda5 rw inMerge 20200312itrd=/Arch3/intel-ucode.img initrd=/Arch3/initramfs-linux.img`.  
The directories are relative the root of the EFI System Parition
1. Create an `nsh` script file in the root directory, like `Arch5.nsh`, to select the right directory and run the boot command.  This can be created using your operating system or using `edit` from the shell itself.  
It's best to do only minor editing in the EFI shell as this can be tedious and error prone.
1. Run the script to boot your operating system.  It is possible to type the whole boot command at the EFI prompt.  Up to you.
1. This is enough to run the everything.  But a Boot manager might be nice.
1. `startup.nsh` in the root of the EFI system drive will be booted by default.  See [Arch's description](https://wiki.archlinux.org/index.php/EFISTUB#Using_a_startup.nsh_script).

Any UEFI specific program can be run within the UEFI shell, say device drivers and the like.

## Boot Managers

Just like for the UEFI shell, you should get these direct from the original providers.  It's a small price to pay to have to manually update them vs the potential to be customized in unusal ways to be overwritten during udpates.

### rEFInd

[rEFInd](http://www.rodsbooks.com/refind/) can be downloaded [here](https://sourceforge.net/projects/refind/files/0.11.5/refind-bin-0.11.5.zip/download).  The `download` file needs to be unzipped.

```shell
cd ~
wget https://sourceforge.net/projects/refind/files/0.11.5/refind-bin-0.11.5.zip/download
unzip download # this is actually the refind-bin-0.11.5.zip file
sudo rsync -r ~/refind-bin-0.11.5/refind/* /boot/efi/refind
mv refind.conf-sample refind.conf
nano refind.conf
cd /boot/efi
efibootmgr -c -l -v refind/refind_x64.efi -L rEFInd
```

Change the boot order back to the original state boot `efibootmgr -o` and refind on the next boot `efibootmgr -n` for testing

<!-- markdownlint-disable MD034 -->
* (https://en.wikipedia.org/wiki/Linux_startup_process)
* (https://en.wikipedia.org/wiki/Initial_ramdisk)
* (https://wiki.archlinux.org/index.php/Arch_boot_process)
* (https://wiki.archlinux.org/index.php/EFISTUB)
* (https://wiki.archlinux.org/index.php/Microcode#EFISTUB)
* (https://glowingthumb.com/uefi-shell-scripts-3-of-3/)
<!-- markdownlint-enable MD034 -->

## Operating Systems

* [Arch Linux](https://www.archlinux.org/) - minimal initial install binary distribution with a good package manager
* [Gentoo linux](https://wiki.gentoo.org/wiki/Main_Page) Source based minimal install
* [Linux From Scratch LFS](http://www.linuxfromscratch.org/) Documentation only installation.  Requires a Linux system.
* [PiLFS](https://intestinate.com/pilfs/guide.html) Pi Linux From Scratch
* [Pi Gentoo](https://wiki.gentoo.org/wiki/Raspberry_Pi)

## Links

* [The Kernel Newbie Corner: "Initrd" And "Initramfs"–What’s Up With That?](https://www.linux.com/tutorials/kernel-newbie-corner-initrd-and-initramfs-whats/)
* [The BIOS/MBR Boot Process](https://neosmart.net/wiki/mbr-boot-process/)
* [Shim and secure boot - fedora](https://docs.fedoraproject.org/en-US/Fedora/18/html/UEFI_Secure_Boot_Guide/sect-UEFI_Secure_Boot_Guide-Implementation_of_UEFI_Secure_Boot-Shim.html)
* [Secure Boot - ubuntu](https://wiki.ubuntu.com/UEFI/SecureBoot)
* [uefi drivers for various file systems](https://efi.akeo.ie/)
* [tianocore releases](https://github.com/tianocore/edk2/releases)
* [Detecting EFI files and Booting them from GRUB](https://forum.manjaro.org/t/detecting-efi-files-and-booting-them-from-grub/38083)
* [Official GNU GRUB Manual](https://www.gnu.org/software/grub/manual/grub/grub.html#Installation)
* [GRUB - Arch](https://wiki.archlinux.org/index.php/GRUB)
* [UEFI startup.nsh script - Arch](https://wiki.archlinux.org/index.php/EFISTUB#Using_a_startup.nsh_script)
* [systemd boot - formerly Gummiboot](https://www.freedesktop.org/wiki/Software/systemd/systemd-boot/)
* [Arch systemd-boot](https://wiki.archlinux.org/index.php/Systemd-boot)
* [Arch boot process](https://wiki.archlinux.org/index.php/Arch_boot_process)
* [Early Userspace in Arch Linux](https://web.archive.org/web/20150430223035/http://archlinux.me/brain0/2010/02/13/early-userspace-in-arch-linux/)
* [Editing GRUB boot entries on startup - press e](https://www.cyberciti.biz/faq/grub-boot-into-single-user-mode/)
* [BIOS/MBR Booting](https://neosmart.net/wiki/mbr-boot-process/)
* [UEFI - Arch](https://wiki.archlinux.org/index.php/Unified_Extensible_Firmware_Interface)
* [UEFI Shell - Arch](https://wiki.archlinux.org/index.php/Unified_Extensible_Firmware_Interface#UEFI_Shell)
* [Official UEFI Specification, including commands](https://uefi.org/sites/default/files/resources/UEFI_Shell_2_2.pdf)
* [Using the UEFI Shell - PDF](https://uefi.org/sites/default/files/resources/Insyde_Using_the_UEFI_Shell.pdf)
* [Binary Release of the UEFI Shell](https://github.com/tianocore/edk2/releases)
* [rEFInd - offical site including lots of useful UEFI, secure boot and related information](http://www.rodsbooks.com/refind/)
* [rEFInd download](https://sourceforge.net/projects/refind/files/0.11.4/)
