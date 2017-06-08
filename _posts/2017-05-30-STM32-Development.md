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
variant without modification. The snippets use the registers very directly which
is useful for their very small code size, clear understanding of how the
software and hardware work together and directly links to the reference manual
for the part: [RM0091: STM32F0x1/STM32F0x2/STM32F0x8 advanced ARM®-based 32-bit
MCUs.](http://www.st.com/resource/en/reference_manual/dm00031936.pdf)

Higher up the development stack, you’ll want to use ST’s own
[STM32CubeMX](http://www.st.com/en/development-tools/stm32cubemx.html) graphical
“initialization code generator” and
[stm32cubef0](http://www.st.com/content/st_com/en/products/embedded-software/mcus-embedded-software/stm32-embedded-software/stm32cube-embedded-software/stm32cubef0.html)
for the example software, drivers and general development support.

You could go the whole hog and get a full fledged IDE. If so, I suggest you take
advantage of a free (as in beer) offer for the F0/L0 processors, like the one
above, for [ARM's Keil Embedded Development
Tools](http://www2.keil.com/stmicroelectronics-stm32) (see this [FAQ from
ST](http://www.st.com/resource/en/product_presentation/faq_stm32f0-l0_discover-webinar_a.pdf)).
That IDE uses ARM’s own excellent compiler, for free.

The [Nucleo variant](https://developer.mbed.org/platforms/ST-Nucleo-F072RB/) of
the development board is compatible with [mbed’s OS
5](https://docs.mbed.com/docs/mbed-os-handbook/en/latest/) and their [free
online compiler](https://developer.mbed.org/compiler/), which is even higher up
the software stack.

Personally I use the [GNU
Toolchains](https://developer.arm.com/open-source/gnu-toolchain/gnu-rm) and
[this](https://github.com/texane/stlink) reverse engineered ST Link with GNU’s
gdb (debugger). That allows me to use the IDE of my choice (Notepad++, VS Code,
Atom, for example) with a little command line fiddling.

Toolchain – GNU ARM - Rough Notes
---------------------------------

download Linux 64-bit version of GNU ARM GCC toolchain 
https://developer.arm.com/open-source/gnu-toolchain/gnu-rm/downloads

open a bash on Windows prompt

`mkdir arm && cd arm`

`tar xvf` the downloaded file

`export arm_bin=~/Downloads/arm/gcc-arm-none-eabi-6-2017-q1-update/bin`

`export PATH=$PATH:$arm_bin`

should be able to run `bash -c "make"` from a windows command prompt, from within the source directory.

Using STMCubeMX
---------------

Code Generator: copy only the necessary library files

- Install STMCubeMX
- run it, pick a board, config, adjust Project Settings
- Toolchain/IDE to Makefile
- Edit project makefile, adjust BINPATH like so:
`BINPATH = ~/Downloads/arm/gcc-arm-none-eabi-6-2017-q1-update/bin `
- Edit the main.c as required.

from the windows command prompt cd to generated source file directory, then compile with `bash -c "make"` 

You can use ST's GUI ST-Link Utility to Program & Verify or the same utilty from the command line the (the cli version)

When the Chip hangs…
--------------------

This was really painful for me because I couldn’t follow the instructions. Here
are my brief notes.

Use the ST supplied Windows [ST-Link
Utility](http://www.st.com/content/st_com/en/products/embedded-software/development-tool-software/stsw-link004.html).
Select menu item Target, Settings. Then pick *Connect Under Reset* (probably
showing *Normal*) in the **Mode** box.
