---
date: "2021-06-14"
title: "Booting Linux and Other Operating Systems"
---

<!-- markdownlint-disable MD025 -->
# Booting Linux and Other Operating Systems
<!-- markdownlint-enable MD025 -->

## Introduction

I want to install multiple operating systems (mostly Linux and Windows) on my computer and choose which one to boot with the without any fuss. I had thought that this was a solved problem. How wrong I was.

I have converted my computers, even the old ones, to UEFI to make things consistent. At a pinch, I can boot MBR disks.

Booting a single operating system isn't trivial - just try to discover, in detail, how it's done for your favourite and you'll see what I mean (for example [Linux bootdisk](https://tldp.org/HOWTO/Bootdisk-HOWTO/index.html)). It's best to use programs that are designed to run in the UEFI environment directly and not things provided by any operating system. Because booting is a critical part of an operating systems, every single system is very particular how they do it and, generally, assumes that they have complete control over every part of the process and usually use a bootloader to do it. This means that operating systems usually interfere with other operating system's ability to boot successfully. [GRUB](https://www.gnu.org/software/grub/manual/grub/grub.html) is a popular choice for bootloader and I've found that Ubuntu's version of GRUB will not boot Arch Linux successfully - giving "Authentication Errors" when I tried to login.

## Booting Sequence

Keeping things simple, I use only UEFI capable hardware.  The process is:

1. Hardware boots, checks its boot order list (kept in NVRAM - non-volatile RAM) and runs the first item.  If that doesn't work, it progresses down the list.
1. If it's an EFI bootable operating system, you're done.
1. If it is a "boot manager" - they're generally not good managers - or "boot loader" - ditto - then this runs and gives its choices.  This process repeats until an operating system is booted.

## Advice

The steps below will ensure that the computer will always boot and that mistakes can be fixed. It requires manually copying files from each operating system's normal boot localion to the EFI system partition. A small price to pay for predictability.

1. Boot from a Linux live or installation USB of some sort
1. Create a 1GB EFI system partition formatted to fat32
1. Install the UEFI shell
1. Install rEFInd
1. Create a startup.nsh script that boots rEFInd
1. Set the boot sequence to the shell first, rEFInd second
1. Copy all operating systems boot files into the system partition
1. Create a UEFI script for the operating system and a startup.nsh for rEFInd
1. Make all copies of Windows UEFI bootable (not a simple process)

## Hardware UEFI Configuration

On older systems, the boot order in the BIOS / UEFI might override any settings applied in software.  For the Shuttle boxes that I use, I had to change the boot to "Windows 8.1/10" from "Windows 7" this disabled a lot of boot choices in the firmware settings.

## EFI Operating System Boot

Find and follow the operating system specific way to boot from EFI directly.  This is the fail safe way to do things.  The information for Arch linux is [here](https://wiki.archlinux.org/index.php/EFISTUB).  Windows and Linux have their own utilities for this: efibootmgr and bcdedit.

### efibootmgr (Linux)

Copy all of the required boot files to their own directory, say `Arch5`, in the EFI system drive and create an EFI shell script to boot it.  

To boot this directly from hardware add an entry to the EFI NVRAM like this:

```shell
efibootmgr -v # check the current boot order
efibootmgr --disk /dev/sda --part 1 --create --label "nuc3arch1" --loader /nuc3arch1/vmlinuz-linux --unicode 'root=UUID=761edd1d-27d0-406a-8033-45c5654dcbc9 rw initrd=/nuc3arch1/intel-ucode.img initrd=/nuc3arch1/initramfs-linux.img' --verbose
efibootmgr -o 0,1 # reset the boot order back to what it was originally
efibootmgr -n 2 # to run the newly added item at next boot
```

#### EIF Booting Windows (bcdedit)

[MBR2GPT command](https://docs.microsoft.com/en-us/windows/deployment/mbr-to-gpt) to convert system drive to EFI.  Move partition to EFI drives by using DD (Linux) or back tool for Windows.

```shell
bcdedit /v
```

## UEFI Shell

I have found that EFI shells, and other pre-opeating system utilities/environments like boot managers, need to be installed from the original sources to work properly.

[TianoCore](https://www.tianocore.org/) provides "an open source implementation of the Unified Extensible Firmware Interface". Releases can be downloaded [here](https://github.com/tianocore/edk2/releases) but these are now source code only. [Feb 2020](https://github.com/tianocore/edk2/releases/download/edk2-stable202002/ShellBinPkg.zip) is the most recent binary release.

```shell
cd ~/Downloads
wget https://github.com/tianocore/edk2/releases/download/edk2-stable202002/ShellBinPkg.zip # The most recent binary version
unzip ShellBinPkg.zip
sudo rsync -r ShellBinPkg/UefiShell /boot/efi/
cd /boot/efi
efibootmgr --disk /dev/sda --part 1 --create --label "TianoCore UEFI Shell" --loader /UefiShell/X64/Shell.efi --verbose
```

Here are some useful EFI commands:

1. `help -b` the -b is for output pagination.
1. `mode` to view and change the number of lines and columns displayed.
1. `map` displays some of the devices available.  On my system there's a series of drives labelled `FS0` (for UEFI known file systems), `BLK1` (block devices), etc.
1. `FS0:` to change to a file system.
1. `ls` to list files, directories.  `cd` change directories

To actually boot things requires that:

1. You know the EFI command to run your operating system.  The command needs to be a single line e.g. [ `vmlinuz-linux root=UUID=761edd1d-27d0-406a-8033-45c5654dcbc9 rw initrd=/nuc3arch1/intel-ucode.img initrd=/nuc3arch1/initramfs-linux.img` ]. The directories are relative the root of the EFI System Partition
1. Create an `nsh` script file in the root directory, like `Arch5.nsh`, to select the right directory and run the boot command.  This can be created using your operating system or using `edit` from the shell itself. Using the EFI shell's `edit` is slow and error prone.
1. Run the script to boot your operating system.  It is possible to type the whole boot command at the EFI prompt.  Up to you.
1. This is enough to run the everything.  But a Boot manager might be nice.
1. `startup.nsh` in the root of the EFI system drive will be booted by default.  See [Arch's description](https://wiki.archlinux.org/index.php/EFISTUB#Using_a_startup.nsh_script).

Any UEFI specific program can be run within the UEFI shell, say device drivers and the like.

## Boot Managers

Just like for the UEFI shell, you should get these direct from the original providers. It's a small price to pay to have to manually update them. If it's installed by an operating system, then you lose control over the boot process - who knows what will happen when the operating system updates itself.

### rEFInd

[rEFInd](http://www.rodsbooks.com/refind/) can be downloaded [here](http://www.rodsbooks.com/refind/getting.html). Once `unzip`ed it needs to be moved to the refind directory on the EFI partition. Linux [quickstart](https://www.rodsbooks.com/refind/linux.html#quickstart) configuration.

```shell
cd ~/Downloads
wget https://sourceforge.net/projects/refind/files/latest/download # it is possible to download it directly like this but not recommended
unzip download # the filename as used by wget (last part)
~/Downloads/refind-bin-0.12.0/mkrlconf # will make a refind_linux.conf in the /boot directory
sudo rsync -r ~/Downloads/refind-bin-0.12.0/refind/* /boot/efi/refind # 12.0 is the current version
efibootmgr --disk /dev/sda --part 1 --create --label "rEFInd" --loader /refind/refind_x64.efi --verbose
```

edit /boot/refind_linux.conf and add `initrd=boot\intel-ucode.img initrd=boot\initramfs-linux.img` to each of the lines.

Might also want to add sample menu items to refind.conf, copied from `refind.conf-sample`, at the bottom of the file.

```bash
menuentry "nuc3arch1" {
    icon     /refind/icons/os_arch.png
    loader   /nuc3arch1/vmlinuz-linux
    initrd   /nuc3arch1/intel-ucode.img
    initrd   /nuc3arch1/initramfs-linux.img
    options  "root=UUID=761edd1d-27d0-406a-8033-45c5654dcbc9 rw"
}

menuentry "nuc3arch1 - just options" {
    icon     /refind/icons/os_arch.png
    loader   /nuc3arch1/vmlinuz-linux
    options  "root=UUID=761edd1d-27d0-406a-8033-45c5654dcbc9 rw initrd=/nuc3arch1/intel-ucode.img initrd=/nuc3arch1/initramfs-linux.img"
}

menuentry "TianoCore UEFI Shell" {
    icon    /refind/icons/tool_shell.png
    loader  /UefiShell/X64/Shell.efi
}
```

Change the boot order back to the original state boot `efibootmgr -o` and refind on the next boot `efibootmgr -n` for testing.

If Arch Linux boots into an emergency shell because it cannot find the root partition, then:

```bash
mount /dev/sda2 new_root # or /dev/disk/by-id/...
exit
```

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

* [Inside the Linux boot process](https://developer.ibm.com/articles/l-linuxboot/)
* [Inspecting the content of an initrd file](https://www.ducea.com/2006/06/24/inspecting-the-content-of-an-initrd-file/)
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
* [rEFInd - official site including lots of useful UEFI, secure boot and related information](http://www.rodsbooks.com/refind/)
