---
date: "2017-07-01"
title: Toolchains and Developer Choice
---

# Toolchains and Developer Choice

When I first started down the Embedded developer route, I imagined that the choice of development tools would be easy. I was used to F\# from Microsoft where you can make your life complicated but an IDE like Visual Studio is a sensible choice. I use [VS Code](https://code.visualstudio.com/) (similar to [Atom](https://atom.io/)) but the truth is that it doesn’t really matter one way or another.

In the embedded world things are very different.

There is the [Arduino](https://www.arduino.cc/) experience with one clear toolchain, one clear IDE and a consistent set of hardware with consistent hardware interfaces. (Much later I discovered that Arduino has simply hidden most things away but I digress.)

[mbed](https://www.mbed.com/en/) (now owned by ARM) is trying to do a similar thing for ARM Cortex based boards more broadly.

There are complete IDEs like [ARM's Keil](http://www.keil.com/) which [is currently free for ST F0 and F1 processors](http://www2.keil.com/stmicroelectronics-stm32).

All of the above hide a lot but you have to read and understand datasheets. That includes the microcontroller one (like [this one from ST](http://www.st.com/resource/en/reference_manual/dm00031936.pdf)) and also for every part you attach to (like [this EEPROM one](http://ww1.microchip.com/downloads/en/DeviceDoc/21231E.pdf)). That means spending a lot of time looking at the various registers under the *Peripherals* -\> *System Viewer* menu.

Given the need to understand the datasheets, the desire to understand what is going on when debugging, and the fact that ARM systems are designed around reading and writing to memory, [David Welch’s](https://github.com/dwelch67) approach of working directly with memory addresses makes a lot of sense (e.g. `PUT32(GPIODBASE+0x18,0xE0001000);` where PUT32 is a tiny function written in assembly language.).

Of course, you can actually write everything in just assembly language but that strikes me as going too far: compilers are designed for this. C is an incredibly versatile language, has stood the test of time, has a low overhead and is very close to the hardware. Why not use it?

## My Preferences

In my 30+ years of computing, I have always wanted to know what is actually going on under the covers. What is necessary, what is abstracted, what is obscured? Tracking down bugs, efficiency and building compact code is a whole lot easier when you understand these things – couple this with a comprehensive IDE and you increase your productivity. One without the other just isn’t as good.

The other factor, for me, is that you can buy a whole Linux system, including WiFi, BlueTooth etc for [less than £10.](https://www.raspberrypi.org/products/raspberry-pi-zero-w/) That means you can do all your high level programming and Internet connectivity using that device with the smaller ARMs giving you direct hardware access and without the complications of pre-emption. Interconnectivity between the Linux host and the ARM device can be provided by SPI, I2C or async. So, with the possible exception of some C++ drivers from the Arduino or similar, there is just no need for programming with a high-level language on the ARM.

## Toolchains

I use the [GNU Toolchain](https://developer.arm.com/open-source/gnu-toolchain/gnu-rm), ST ST-Link tool and [VS Code](https://code.visualstudio.com/).

For GDB debugging use SEGGER’s [J-Link for ST-Link on board](https://www.segger.com/products/debug-probes/j-link/models/other-j-links/st-link-on-board/?L=0) or [this](https://github.com/texane/stlink) reverse engineered ST Link.

With this setup, you can use pretty much anything for development (Notepad++, VS Code, Atom, for example) with a little command line fiddling.

# Toolchain – GNU ARM - Rough Notes

download Linux 64-bit version of GNU ARM GCC toolchain https://developer.arm.com/open-source/gnu-toolchain/gnu-rm/downloads

open a bash on Windows prompt

```bash
mkdir arm && cd arm
tar -xvf # the downloaded file
export arm_bin=~/Downloads/arm/gcc-arm-none-eabi-6-2017-q1-update/bin`
export PATH=$PATH:$arm_bin
```

should be able to run `bash -c "make"` from a windows command prompt, from within the source directory.

## Using STMCubeMX

Code Generator: copy only the necessary library files

-  Install STMCubeMX
-  run it, pick a board, config, adjust Project Settings
-  Toolchain/IDE to Makefile
-  Edit project makefile, adjust BINPATH like so: `BINPATH =
    ~/Downloads/arm/gcc-arm-none-eabi-6-2017-q1-update/bin`
-  Edit the main.c as required.
-  Remove all the extra source files that you don't need. The bare minimum

```bash
C_SOURCES =  \
Src/system_stm32f0xx.c \
Src/main.c \
Src/morse.c
```

from the windows command prompt cd to generated source file directory, then compile with

`bash -c "make"`

You can use ST's GUI ST-Link Utility to Program & Verify or the same utilty from the command line the (the cli version). E.g.

`"C:\\Program Files (x86)\\STMicroelectronics\\STM32 ST-LINK Utility\\ST-LINK Utility\\ST-Link\_CLI.exe" -me -p build\\try.hex -v -rst`

(-me = full chip erase, -p program the following file, -v verify, -rst reset the chip)

## When the Chip hangs…

This was really painful for me because I couldn’t follow these instructions: use the ST supplied Windows [ST-Link Utility](http://www.st.com/content/st_com/en/products/embedded-software/development-tool-software/stsw-link004.html). Select menu item Target, Settings. Then pick *Connect Under Reset* (probably currently showing *Normal*) in the **Mode** box.
