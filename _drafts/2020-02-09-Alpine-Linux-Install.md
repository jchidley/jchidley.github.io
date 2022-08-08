---
---

<!-- markdownlint-disable MD025 -->
# Alpine Linux Install
<!-- markdownlint-enable MD025 -->

## Introduction

What makes [Alpine Linux](https://alpinelinux.org/about/) interesting? It is an extremely lightweight and easy to configure system. To really appreaciate just what it offers an administrator look at [these system backup instructions](https://wiki.alpinelinux.org/wiki/Back_Up_a_Flash_Memory_Installation). To build a new system, based on an existing one, take a backup (or use a vanilla [installation file](https://alpinelinux.org/downloads/)), edit or write [the configuration file - AKA apkvol](https://wiki.alpinelinux.org/wiki/Manually_editing_a_existing_apkovl) and add the necessary packages to both [the local cache](https://wiki.alpinelinux.org/wiki/Local_APK_cache) and the `/etc/apk/world` file. `lbu commit` and you are done.

[This guide](https://wiki.alpinelinux.org/wiki/Alpine_Source_Map_by_boot_sequence) describes how Alpine Linux boots. Finally, if you're missing a favourite command then `akp search [faviourite missing command]` is what you need before you `apk add [found package name]`.

For more detailed information see the [Alpine User Handbook](https://docs.alpinelinux.org/user-handbook/0.1a/index.html) and the [Developer Documentation](https://wiki.alpinelinux.org/wiki/Category_talk:Developer_Documentation).

This is the Linux that I have been waiting for.

## From Scratch Install - Intel Desktop

boot USB (or other prepared) boot device and run the setup program

```bash
setup-alpine
```

I manually configured the partitions because I'm running an EFI system.

### EFI boot

create `.nsh` file like this:

```bash
fs0:
cd /alpine1shuttle1
vmlinux ... root... modules... initrd=/alpine1shuttle1/initramfs-lts
```

The boot line is modified from the extlinux.cfg file. Note the initrd comes at the end and includes the full path on the EFI system drive.

### xfce4 desktop

```bash
setup-xorg-base xfce4 xfce4-terminal lightdm-gtk-greeter xfce-polkit xfce4-screensaver consolekit2 dbus-x11 sudo
vi /etc/apk/repositories
```

<!-- markdownlint-disable MD034 -->
uncomment http://dl-cdn.alpinelinux.org/alpine/edge/community or similar
<!-- markdownlint-enable MD034 -->

```bash
apk update
apk add xf86-video-intel # already added
apk add xf86-input-mouse xf86-input-keyboard
setxkbmap gb
adduser -g 'jack' jack
addgroup jack wheel
visudo
lbu include /home
rc-service dbus start # temp
rc-service lightdm start # temp
rc-update add dbus # rebooted
rc-update add lightdm # rebooted
```

### Firefox

```bash
apk add firefox-esr
```

### The End

This is enough to get a normal desktop in under 2G of disk space.

## Links

* [XFCE Setup](https://wiki.alpinelinux.org/wiki/XFCE_Setup)
* [Enable Community Repository](https://wiki.alpinelinux.org/wiki/Enable_Community_Repository)
<!-- markdownlint-disable MD034 -->
https://serverfault.com/a/821235
<!-- markdownlint-enable MD034 -->

### Make your own ISO

[How to make a custom ISO image with mkimage](https://wiki.alpinelinux.org/wiki/How_to_make_a_custom_ISO_image_with_mkimage) - note that the architecture has to be the same as the host.

```bash
apk add alpine-sdk build-base apk-tools alpine-conf busybox fakeroot xorriso squashfs-tools sudo mtools dosfstools
adduser build -G abuild
echo "%abuild ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/abuild
abuild-keygen -i -a
git clone https://gitlab.alpinelinux.org/alpine/aports.git
sudo apk update
export PROFILENAME=minimal

cat << EOF > ~/aports/scripts/mkimg.$PROFILENAME.sh
profile_$PROFILENAME() {
        profile_standard
        kernel_cmdline="unionfs_size=512M console=tty0 console=ttyS0,115200"
        syslinux_serial="0 115200"
        kernel_addons=""
        apks="\$apks mdadm mkinitfs mtools rsync sfdisk 
                util-linux dosfstools ntfs-3g"
        local _k _a
        for _k in \$kernel_flavors; do
                apks="\$apks linux-\$_k"
                for _a in \$kernel_addons; do
                        apks="\$apks \$_a-\$_k"
                done
        done
        apks="\$apks linux-firmware"
}
EOF

cd ~/aports/scripts
chmod +x mkimg.$PROFILENAME.sh
mkdir -p ~/iso

sh mkimage.sh --tag edge \
  --outdir ~/iso \
  --arch armv7 \
  --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
  --profile $PROFILENAME
```

[Pro Terminal Commands: Using diskutil](https://applegazette.com/mac/pro-terminal-commands-using-diskutil/)

```mac
diskutil listFilesystems
diskutil list
diskutil eraseDisk MS-DOS ALPINE disk§
diskutil partitionDisk disk§ 2 MBR MS-DOS ALPINE 512MB MS-DOS DATA R
```

Notes about apk cache [Alpine local backup](https://wiki.alpinelinux.org/wiki/Alpine_local_backup)

<!-- markdownlint-disable MD034 -->
<!-- markdownlint-enable MD034 -->

[Back Up a Flash Memory Installation](https://wiki.alpinelinux.org/wiki/Back_Up_a_Flash_Memory_Installation)
[Manually editing a existing apkovl](https://wiki.alpinelinux.org/wiki/Manually_editing_a_existing_apkovl)
[Local APK cache](https://wiki.alpinelinux.org/wiki/Local_APK_cache)
[Alpine Source Map by boot sequence](https://wiki.alpinelinux.org/wiki/Alpine_Source_Map_by_boot_sequence)

[Alpine Linux APK off-line overlay builder](https://github.com/rnalrd/apkovl-builder/blob/master/create_apkovl.sh)
[Automated provisioning using apkovl](https://blog.w1r3.net/2018/04/16/automated-provisioning-using-apkovl.html)
[Create a bootable SDHC from a Mac](https://wiki.alpinelinux.org/wiki/Create_a_bootable_SDHC_from_a_Mac)

[Semi-Automatic Installation](https://docs.alpinelinux.org/user-handbook/0.1a/Installing/manual.html#_repositories)
[Alpine Linux Install](https://wiki.alpinelinux.org/wiki/Installation)
[How to make a custom ISO image with mkimage](https://wiki.alpinelinux.org/wiki/How_to_make_a_custom_ISO_image_with_mkimage)
[Directly booting an ISO file](https://wiki.alpinelinux.org/wiki/Directly_booting_an_ISO_file)
[QEMU](https://wiki.alpinelinux.org/wiki/Qemu)
[10 Alpine Linux apk Command Examples](https://www.cyberciti.biz/faq/10-alpine-linux-apk-command-examples/)
[How to get regular stuff working](https://wiki.alpinelinux.org/wiki/How_to_get_regular_stuff_working)
