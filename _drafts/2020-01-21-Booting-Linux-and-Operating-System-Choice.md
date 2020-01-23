2020-01-21-Booting-Linux-and-Operating-System-Choice

---

date: "2020-01-15"
title: "Booting Linux and Operating System Choice"
---

# Booting Linux and Operating System Choice

## Introduction

All I want to to install multiple operating systems on my computer and then choose which one to start at
boot time.  I had thought that this was a solved problem.  How wrong I was.

I am talking about booting a relativly modern desktop system.  Specifically Linux and Windows.

## Booting Sequence

At hardware power on, what is needed is to select an operating system and boot it.  Most hardware now uses EFI
and what is booted is a process.  A simple overview is:

1. Hardware searches the EFI data and calls the first entry in the list in nvram.  If that doesn't work, it
2. moves to the next entry.
3. If the EFI entry is a bootable opeating system, it boots and you're done.
4. If it is a boot manager, it then has it's own method of chosing what to boot next.  What's booted next could be another operating system, a boot manager or something else.

## EFI Booting

A modern computer uses EFI to boot.  In linux you can see what it's booting using ```efibootmgr -v``` and
and use ```efibootmgr -n``` to tell the computer what to boot next.  A system that only uses efibootmgr (or
the windows eqivalent  ```bcdedit```) would require the use of the command line and be entirely predictable.

### efibootmgr 

This is how you can add an entry to the EFI nvram

```efibootmgr --disk /dev/sda --part 1 --create --label "Arch 5" --loader /Arch5/vmlinuz-linux --unicode 'root=UUID=23aff7da-45d6-492d-9f9c-b71b531cebfb rw initrd=/Arch5/initramfs-linux.img' --verbose```

## UEFI Shell

https://efi.akeo.ie/ uefi drivers for various file systems

## Linux Boot

https://www.linux.com/tutorials/kernel-newbie-corner-initrd-and-initramfs-whats/
https://en.wikipedia.org/wiki/Linux_startup_process
https://en.wikipedia.org/wiki/Initial_ramdisk
https://wiki.archlinux.org/index.php/Arch_boot_process 
https://wiki.archlinux.org/index.php/EFISTUB
https://wiki.archlinux.org/index.php/Microcode#EFISTUB

## Links
https://github.com/tianocore/edk2/releases 
* https://uefi.org/sites/default/files/resources/Insyde_Using_the_UEFI_Shell.pdf
* https://sourceforge.net/projects/refind/files/0.11.4/
* https://glowingthumb.com/uefi-shell-scripts-3-of-3/
* https://wiki.archlinux.org/index.php/EFISTUB#Using_a_startup.nsh_script 
https://wiki.archlinux.org/index.php/Unified_Extensible_Firmware_Interface#UEFI_Shell 
https://wiki.archlinux.org/index.php/Systemd-boot 
https://www.freedesktop.org/wiki/Software/systemd/systemd-boot/ 

* [Arch boot process](https://wiki.archlinux.org/index.php/Arch_boot_process)
* [Early Userspace in Arch Linux](https://web.archive.org/web/20150430223035/http://archlinux.me/brain0/2010/02/13/early-userspace-in-arch-linux/)
* [Editing GRUB boot entries on startup - press e](https://www.cyberciti.biz/faq/grub-boot-into-single-user-mode/)
* [BIOS/MBR Booting](https://neosmart.net/wiki/mbr-boot-process/)
* [UEFI](https://wiki.archlinux.org/index.php/Unified_Extensible_Firmware_Interface)
* [UEFI Shell](https://wiki.archlinux.org/index.php/Unified_Extensible_Firmware_Interface#UEFI_Shell)
* [Using the UEFI Shell - PDF](https://uefi.org/sites/default/files/resources/Insyde_Using_the_UEFI_Shell.pdf)
* [Binary Release of the UEFI Shell](https://github.com/tianocore/edk2/releases)
