---
date: "2020-01-28"
title: "File systems"
---
<!-- 2020-01-27-Simplest-possible-Linux-boot -->

<!-- markdownlint-disable MD025 -->
# File systems
<!-- markdownlint-enable MD025 -->

## Introduction

## Working with Windows

Turn off faststart by:

```cmd
powercfg /h off
```

Use [NTFS-3G](https://www.tuxera.com/community/ntfs-3g-faq/) to share data with Windows and Linux.  [Here is Arch Linux' information](https://wiki.archlinux.org/index.php/NTFS-3G).

```bash
pacman -S ntfs-3g
mkfs.ntfs # no need to be explicit in Arch Linux
mount /dev/sda2 /mnt # Arch linux support
```

In `/etc/fstab`:

```bash
# <file system>		<dir>		<type>	<options>	<dump>	<pass>
/dev/NTFS-part		/mnt/windows	ntfs-3g	defaults	0	0
```

## Links

* [Creating and using squashed file systems](https://www.tldp.org/HOWTO/SquashFS-HOWTO/creatingandusing.html)
* [Overlay filesystem](https://wiki.archlinux.org/index.php/Overlay_filesystem)
* [Overlay Filesystes](https://www.kernel.org/doc/Documentation/filesystems/overlayfs.txt)
* [Full system backup with SquashFS](https://wiki.archlinux.org/index.php/Full_system_backup_with_SquashFS)
* [MBR file system identifiers](https://www.win.tue.nl/~aeb/partitions/partition_types-1.html)
* [Example OverlayFS Usage](https://askubuntu.com/questions/699565/example-overlayfs-usage)
* [OverlayFS](https://blog.programster.org/overlayfs)
* [How do I use OverlayFS](https://askubuntu.com/questions/109413/how-do-i-use-overlayfs/109441#109441)
* [Playing with overlayfs](http://jasonwryan.com/blog/2015/01/19/overlayfs/)
* [a practical look into overlayfs](https://ops.tips/notes/practical-look-into-overlayfs/)

<!-- markdownlint-disable MD034 -->
* https://askubuntu.com/questions/699565/example-overlayfs-usage
https://www.thegeekstuff.com/2017/05/sfdisk-examples/
https://wiki.archlinux.org/index.php/Fdisk
https://wiki.archlinux.org/index.php/GPT_fdisk#Convert_between_MBR_and_GPT
<!-- markdownlint-enable MD034 -->
