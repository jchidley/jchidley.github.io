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
2. If it's an EFI bootable operating system, you're done.
3. If it is a "boot manager" - they're generally not good managers - or "boot loader" - ditto - then this runs and gives its choices.  This process repeats until an operating system is booted.

Things can get complicated.  This is what to do in order:

1. Check Hardware is configured for EFI
1. Make sure that you can boot your operating system directly from UEFI - see EFI Operating System Boot
1. Install a command line shell so that you can repair anything that goes wrong, and boot things - see EFI Shell
1. Try your luck with a friendlier method of booting - see Boot Managers 

## Hardare UEFI Configuration

On older systems, the boot order in the BIOS / UEFI might override any settings applied in software.  For the older Shuttle boxes that I use, I had to change the boot to "Windows 8.1/10" from "Windows 7" this disabled a lot of boot choices in the firmware settings.

## EFI Operating System Boot

Find and follow the operating system specific way to boot from EFI directly.  This is the fail safe way to do things.  The information for Arch linux is [here](https://wiki.archlinux.org/index.php/EFISTUB).  Windows and Linux have their own utilities for this efibootmgr and bcdedit.

### efibootmgr (Linux)

Copy all of the required boot files to their own directory, say ```Arch5```, in the EFI system drive (e.g. first drive and first partition ```--disk /dev/sda --part 1```) and then add an entry to the EFI nvram like this:

````shell
efibootmgr -v # check the current boot order
efibootmgr --disk /dev/sda --part 1 --create --label "Arch 5" --loader /Arch5/vmlinuz-linux --unicode 'root=UUID=23aff7da-45d6-492d-9f9c-b71b531cebfb rw initrd=/Arch5/initramfs-linux.img' --verbose
# assuming that it's adding it as item Boot0002 and that there were Boot0000 and Boot0001 before
efibootmgr -o 0,1 # reset the boot order back to what it was orginally
efibootmgr -n 2 # to run the newly added item at next boot
````

#### bcdedit (Windows)

````shell
bcdedit /v
````

## UEFI Shell

I have found that shells, and other pre-opeating system utilties/enviroments like boot managers, need to be installed from the original sources.  Operating system providers tend to customise these things and hence they don't always play well with other operating systems.

[TianoCore](https://www.tianocore.org/) provides "an open source implementation of the Unified Extensible Firmware Interface" and a release can be downloaded [here](https://github.com/tianocore/edk2/releases).  I put mine in the root of my EFI partion in /Uefishell and ran this to add it to NVRAM, same process as to add an operating system, above.

````shell
efibootmgr --disk /dev/sda --part 1 --create --label "TianoCore UEFI Shell" --loader /Uefishell/Shell.efi --verbose
````

Note that this is a single long line.

Here are some useful shell commands:
1. ```help -b``` the -b is for output pagination.
2. ```mode``` to view and change the number of lines and columns displayed.
3. ```map``` displays some of the devices available.  On my system there's a series of drives labelled ```FS0```, ```BLK1```, etc.
4. ```FS0:``` to change to a drive
5. ```ls``` to list files, directories.  ```cd``` change directories

To actually boot things requires that:
1. You know the EFI command to run your operating system.  The command needs to be a single line e.g.  
```vmlinuz-linux root=/dev/sda5 rw initrd=/Arch3/intel-ucode.img initrd=/Arch3/initramfs-linux.img```.  
The directories are relative the root of the EFI System Parition

1. Create an ```nsh``` script file in the root directory, like ```Arch5.nsh```, to select the right directory and run the boot command.  This can be created using your operating system or using ```edit``` from the shell itself.  
It's best to do only minor editing in the EFI shell as this can be tedious and error prone.
1. Run the script to boot your operating system.  It is possible to type the whole boot command at the EFI prompt.  Up to you.
1. This is enough to run the everything.  But a Boot manager might be nice.
1. ```startup.nsh``` in the root of the EFI system drive will be booted by default.  See [Arch's description](https://wiki.archlinux.org/index.php/EFISTUB#Using_a_startup.nsh_script).

Any UEFI specific program can be run within the UEFI shell, say device drivers and the like.

## Boot Managers

Just like for the UEFI shell, you should get these direct from the original providers.  It's a small price to pay to have to manually update them vs the potential to be customized in unusal ways to be overwritten during udpates.

### rEFInd

[rEFInd](http://www.rodsbooks.com/refind/) can be downloaded [here](https://sourceforge.net/projects/refind/files/0.11.4/refind-bin-0.11.4.zip/download)
 
````shell
unzip refind-bin-0.11.4.zip
rsync -r /home/jack/Downloads/refind-bin-0.11.4/refind/* refind
mv refind.conf-sample refind.conf
nano refind.conf
efibootmgr -c -l \\refind\\refind_x64.efi -L rEFInd
# change the boot order back, boot refind next for testing
````

<!-- markdownlint-disable MD034 -->
* (https://www.linux.com/tutorials/kernel-newbie-corner-initrd-and-initramfs-whats/)
* (https://en.wikipedia.org/wiki/Linux_startup_process)
* (https://en.wikipedia.org/wiki/Initial_ramdisk)
* (https://wiki.archlinux.org/index.php/Arch_boot_process)
* (https://wiki.archlinux.org/index.php/EFISTUB)
* (https://wiki.archlinux.org/index.php/Microcode#EFISTUB)

## Links

* [uefi drivers for various file systems](https://efi.akeo.ie/)
* [tianocore releases](https://github.com/tianocore/edk2/releases)
* (https://uefi.org/sites/default/files/resources/Insyde_Using_the_UEFI_Shell.pdf)
* (https://sourceforge.net/projects/refind/files/0.11.4/)
* (https://glowingthumb.com/uefi-shell-scripts-3-of-3/)
* (https://wiki.archlinux.org/index.php/EFISTUB#Using_a_startup.nsh_script)
* (https://wiki.archlinux.org/index.php/Unified_Extensible_Firmware_Interface#UEFI_Shell)
* (https://wiki.archlinux.org/index.php/Systemd-boot)
* (https://www.freedesktop.org/wiki/Software/systemd/systemd-boot/)
<!-- markdownlint-enable MD034 -->
* [Arch boot process](https://wiki.archlinux.org/index.php/Arch_boot_process)
* [Early Userspace in Arch Linux](https://web.archive.org/web/20150430223035/http://archlinux.me/brain0/2010/02/13/early-userspace-in-arch-linux/)
* [Editing GRUB boot entries on startup - press e](https://www.cyberciti.biz/faq/grub-boot-into-single-user-mode/)
* [BIOS/MBR Booting](https://neosmart.net/wiki/mbr-boot-process/)
* [UEFI](https://wiki.archlinux.org/index.php/Unified_Extensible_Firmware_Interface)
* [UEFI Shell](https://wiki.archlinux.org/index.php/Unified_Extensible_Firmware_Interface#UEFI_Shell)
* [Using the UEFI Shell - PDF](https://uefi.org/sites/default/files/resources/Insyde_Using_the_UEFI_Shell.pdf)
* [Binary Release of the UEFI Shell](https://github.com/tianocore/edk2/releases)