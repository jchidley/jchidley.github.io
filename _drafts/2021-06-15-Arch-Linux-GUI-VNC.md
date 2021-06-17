---
date: "2021-06-15"
title: "Arch Linux GUI VNC"
---

<!-- markdownlint-disable MD025 -->
# Arch Linux Installation
<!-- markdownlint-enable MD025 -->

## Introduction

My pithy guide to setup Arch Linux. The official Arch installation instructions are on the [Wiki](https://wiki.archlinux.org/index.php/Installation_guide).

## GUI

pacman -S base-devel

```bash
pacman -S xorg-server xfce4
pacman -S xf86-video-intel # card specific video drivers
pacman -S nvidia-390xx # legacy driver front room
pacman -S xorg-xinit # startx
localectl --no-convert set-x11-keymap gb # UK keyboard layout
setxkbmap gb # X11 current session only
```

[sara - lightweight tiling window manager](https://github.com/gitluin/sara)

```bash
pacman -S libxft libxinerama # and for dmenu
git clone https://github.com/gitluin/sara.git
cd sara
cp config.def.h config.h
sed -i -E 's/barpx\s+=\s+18/barpx\t\t\t= 0/g' config.h # set top bar to 0
grep barpx config.h # check
make
sudo make install
```

[st - fork of suckless' simple terminal](https://github.com/LukeSmithxyz/st) as there would be no terminal otherwise

```bash
pacman -S libxext ncurses # from sara install libxft
git clone https://github.com/LukeSmithxyz/st.git
```

[dmenu - "super+d" for mini menu](https://tools.suckless.org/dmenu/)

```bash
# same requirement as sara
git clone https://git.suckless.org/dmenu
```

[sxhkd - X daemon for input events - keyboard, mouse](https://github.com/baskerville/sxhkd)

```bash
pacman -S libxcb xcb-util-keysyms xcb-util
git clone https://github.com/baskerville/sxhkd.git
cd sxhkd
make
sudo make install
mkdir -p ~/.config/sxhkd
cp ~/sara/examples/sxhkdrc ~/.config/sxhkd/sxhkdrc
```

`~/.xinitrc`

```bash
setxkbmap -layout gb
sxhkd -c & # enable keys e.g. 'super-d' for dmenu
st & # start with a terminal on screen
exec sara # or another display manager
```

If you don't load the correct drivers, you get an unhelpful set of errors including `xinit: unable to connect to X server: Connection refused`. Also, don’t run X as root.

```bash
pacman -S firefox # web browser
```

## bash config

Things to add to `~/.bash_profile`, which ones on first login:

```bash
tbsm # needs to be last
```

`~/.bashrc` which runs on every interactive shell

```bash
source ~/basic-env/bin/activate # enable a default Python environment to avoid polluting everything
```

## VNC

If you use localhost in your VNC config then you will have to use ssh as a tunnel or VNC will not work remotely. Or turn off localhost and transmit in clear.

* [TigerVNC - ArchWiki](https://wiki.archlinux.org/title/TigerVNC)
* [CustomXSession - Ubuntu Wiki](https://wiki.ubuntu.com/CustomXSession)
* [gdm - How do I replace the desktop by an application? - Ask Ubuntu](https://askubuntu.com/questions/23932/how-do-i-replace-the-desktop-by-an-application)
* [Display manager - ArchWiki](https://wiki.archlinux.org/title/Display_manager)
* [xinit - ArchWiki](https://wiki.archlinux.org/title/Xinit)
* [Xorg - ArchWiki](https://wiki.archlinux.org/title/Xorg#Session_log_redirection)
* [GitHub - evertiro/cdm: Console Display Manager](https://github.com/evertiro/cdm)
* [AUR (en) - udm](https://aur.archlinux.org/packages/udm)

## Links

* [Intel Graphics](https://wiki.archlinux.org/index.php/intel_graphics)
* [AUR - Arch User Repository](https://wiki.archlinux.org/index.php/Arch_User_Repository)
* [tbsm - minimal display manager](https://aur.archlinux.org/packages/tbsm/)
* [st - simple terminal](https://st.suckless.org)
* [GitHub - gitluin/sara: Originally a fork of catwm, now an offspring of dwm with a streamlined featureset, plus some bspwm.](https://github.com/gitluin/sara)
* [Alacritty - graphics accellerated terminal](https://github.com/alacritty/alacritty)
* [st fonts](https://wiki.archlinux.org/index.php/st#Font)
* [Symbol fonts for linux terminals](https://c42f.github.io/2015/12/29/crisp-terminal-fonts.html)
* [Fonts - Arch Linux](https://wiki.archlinux.org/index.php/Fonts#Font_packages)
