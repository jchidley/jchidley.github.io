---
date: "2017-05-30"
title: STM32 Development
---

STM32 Development
=================

You’ll want to read [this online
book](https://www.cs.indiana.edu/~geobrown/book.pdf) and [this excellent
blog](http://blog.mark-stevens.co.uk/?s=stm32), which are a little dated but
still relevant. You can follow along, with some changes, with these [parts from
ST](http://www.st.com/content/st_com/en/search.html#q=STM32F072RB-t=keywords-page=1)
based on the
[STM32F072RB](http://www.st.com/content/st_com/en/products/microcontrollers/stm32-32-bit-arm-cortex-mcus/stm32f0-series/stm32f0x2/stm32f072rb.html)
processor. I suggest the cheap and functional
[32F072BDISCOVERY](http://www.st.com/content/st_com/en/products/evaluation-tools/product-evaluation-tools/mcu-eval-tools/stm32-mcu-eval-tools/stm32-mcu-discovery-kits/32f072bdiscovery.html)
development board (add the optional
[NUCLEO-F072RB](http://www.st.com/content/st_com/en/products/evaluation-tools/product-evaluation-tools/mcu-eval-tools/stm32-mcu-eval-tools/stm32-mcu-nucleo/nucleo-f072rb.html)
board to make your [mbed](https://www.mbed.com/en/) life simpler, if you go down
that route).

The really useful
[STM32SnippetsF0](http://www.st.com/content/st_com/en/products/embedded-software/mcus-embedded-software/stm32-embedded-software/stm32snippets/stm32snippetsf0.html)
are written for the discovery board above and will probably work for the Nucleo
variant without modification. The snippets use the registers directly which is
good for their very small code size, clear understanding of how the software and
hardware work together and direct relationship with the reference manual:
[RM0091: STM32F0x1/STM32F0x2/STM32F0x8 advanced ARM®-based 32-bit
MCUs.](http://www.st.com/resource/en/reference_manual/dm00031936.pdf)

I found an extremely cheap STM32F030F4P6 break-out board – including an external
8Mhz clock - on ebay (e.g. “STM32F030F4P6 Minimum System Board”) for \$1.69 /
£1.30 to experiment on. You need to use the ST-Link on your Discovery or Nucleo
to program and debug it.

Higher up the development stack, you may want to use ST’s own
[STM32CubeMX](http://www.st.com/en/development-tools/stm32cubemx.html) graphical
“initialization code generator” and
[stm32cubef0](http://www.st.com/content/st_com/en/products/embedded-software/mcus-embedded-software/stm32-embedded-software/stm32cube-embedded-software/stm32cubef0.html)
for the example software, drivers and general development support. These tools
will give you usable code that shows you how things can be done. But the code
generated can be unnecessarily long, with a lot of abstraction, making it
difficult to follow and, according to some sources, it can be buggy too.

You could go the whole hog and get a IDE. If so, I suggest you take advantage of
a free (as in beer) offer for the F0/L0 processors for [ARM's Keil Embedded
Development Tools](http://www2.keil.com/stmicroelectronics-stm32) (see this [FAQ
from
ST](http://www.st.com/resource/en/product_presentation/faq_stm32f0-l0_discover-webinar_a.pdf)).
That IDE uses ARM’s own excellent compiler, for free.

The [Nucleo variant](https://developer.mbed.org/platforms/ST-Nucleo-F072RB/) of
the development board is compatible with [mbed’s OS
5](https://docs.mbed.com/docs/mbed-os-handbook/en/latest/) and their [free
online compiler](https://developer.mbed.org/compiler/), which is even higher up
the software stack.

I use the [GNU
Toolchain](https://developer.arm.com/open-source/gnu-toolchain/gnu-rm), ST
ST-Link tool and [VS Code](https://code.visualstudio.com/).

For GDB debugging use SEGGER’s [J-Link for ST-Link on
board](https://www.segger.com/products/debug-probes/j-link/models/other-j-links/st-link-on-board/?L=0)
or [this](https://github.com/texane/stlink) reverse engineered ST Link.

With this setup, you can use pretty much anything for development (Notepad++, VS
Code, Atom, for example) with a little command line fiddling.

Toolchain – GNU ARM - Rough Notes
---------------------------------

download Linux 64-bit version of GNU ARM GCC toolchain
https://developer.arm.com/open-source/gnu-toolchain/gnu-rm/downloads

open a bash on Windows prompt

`mkdir arm && cd arm`

`tar xvf` the downloaded file

`export arm_bin=~/Downloads/arm/gcc-arm-none-eabi-6-2017-q1-update/bin`

`export PATH=$PATH:$arm_bin`

should be able to run `bash -c "make"` from a windows command prompt, from
within the source directory.

Using STMCubeMX
---------------

Code Generator: copy only the necessary library files

-   Install STMCubeMX

-   run it, pick a board, config, adjust Project Settings

-   Toolchain/IDE to Makefile

-   Edit project makefile, adjust BINPATH like so: `BINPATH =
    ~/Downloads/arm/gcc-arm-none-eabi-6-2017-q1-update/bin`

-   Edit the main.c as required.

-   Remove all the extra source files that you don't need. The bare minimum is:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
C_SOURCES =  \
Src/system_stm32f0xx.c \
Src/main.c \
Src/morse.c
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from the windows command prompt cd to generated source file directory, then
compile with

`bash -c "make"`

You can use ST's GUI ST-Link Utility to Program & Verify or the same utilty from
the command line the (the cli version). E.g.

`"C:\\Program Files (x86)\\STMicroelectronics\\STM32 ST-LINK Utility\\ST-LINK
Utility\\ST-Link\_CLI.exe" -me -p build\\try.hex -v -rst`

(-me = full chip erase, -p program the following file, -v verify, -rst reset the
chip)

When the Chip hangs…
--------------------

This was really painful for me because I couldn’t follow these instructions: use
the ST supplied Windows [ST-Link
Utility](http://www.st.com/content/st_com/en/products/embedded-software/development-tool-software/stsw-link004.html).
Select menu item Target, Settings. Then pick *Connect Under Reset* (probably
currently showing *Normal*) in the **Mode** box.
