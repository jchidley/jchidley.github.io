---
date: "2017-05-30"
title: STM32 Development
---

# STM32 Development

[This online book](https://www.cs.indiana.edu/~geobrown/book.pdf), [this excellent blog](http://blog.mark-stevens.co.uk/?s=stm32) and this [YouTube delivered "Embedded Systems Programming Course"](https://www.youtube.com/playlist?list=PLfcIZXsDLA1-QEyrD4R9YcWWKpbCcrGVP&app=desktop) are a little dated but still relevant. It’s possible to follow along using [current parts from ST](http://www.st.com/). Today’s best option seems to be the cheap and functional [32F072BDISCOVERY](http://www.st.com/content/st_com/en/products/evaluation-tools/product-evaluation-tools/mcu-eval-tools/stm32-mcu-eval-tools/stm32-mcu-discovery-kits/32f072bdiscovery.html) development board (the optional [NUCLEO-F072RB](http://www.st.com/content/st_com/en/products/evaluation-tools/product-evaluation-tools/mcu-eval-tools/stm32-mcu-eval-tools/stm32-mcu-nucleo/nucleo-f072rb.html) board makes [mbed](https://www.mbed.com/en/) simpler, if you go down that route) both of which are based on the [STM32F072RB](http://www.st.com/content/st_com/en/products/microcontrollers/stm32-32-bit-arm-cortex-mcus/stm32f0-series/stm32f0x2/stm32f072rb.html) processor.

The really useful [STM32SnippetsF0](http://www.st.com/content/st_com/en/products/embedded-software/mcus-embedded-software/stm32-embedded-software/stm32snippets/stm32snippetsf0.html) are written for the discovery board above and work for the Nucleo variant with minor modifications. The snippets use the registers directly which is good for their very small code size, clear understanding of how the software and hardware work together and direct relationship with the reference manual: [RM0091: STM32F0x1/STM32F0x2/STM32F0x8 advanced ARM®-based 32-bit MCUs.](http://www.st.com/resource/en/reference_manual/dm00031936.pdf)

I found an extremely cheap STM32F030F4P6 break-out board for experiments on eBay –\$1.69 / £1.30 including headers, usb for power and an 8MHz clock search “STM32F030F4P6 Minimum System Board”. The ST-Link on the Discovery or Nucleo can be used to program or debug it.

The easiest way to program and debug is to use an IDE. Currently there is a free (as in beer) offer for the F0/L0 processors for [ARM's Keil Embedded Development Tools](http://www2.keil.com/stmicroelectronics-stm32) (see this [FAQ from ST](http://www.st.com/resource/en/product_presentation/faq_stm32f0-l0_discover-webinar_a.pdf)). That IDE uses ARM’s own excellent compiler, for free.

The [Nucleo variant](https://developer.mbed.org/platforms/ST-Nucleo-F072RB/) of the development board is compatible with [mbed’s OS 5](https://docs.mbed.com/docs/mbed-os-handbook/en/latest/) and their [free online compiler](https://developer.mbed.org/compiler/). It is possible to use mbed’s system without their online compiler or tooling see [David Welch's mbed samples on GitHub](https://github.com/dwelch67/mbed_samples/blob/master/blinker01/README.blinker01.txt).

ST’s [STM32CubeMX](http://www.st.com/en/development-tools/stm32cubemx.html) graphical “initialization code generator” and [stm32cubef0](http://www.st.com/content/st_com/en/products/embedded-software/mcus-embedded-software/stm32-embedded-software/stm32cube-embedded-software/stm32cubef0.html) provide example software, drivers and general development support which can then be used with a variety of toolchains (including GNU – Makefile). This is helpful from the point of view of samples and ideas but the generated code can be very long, with a lot of abstraction, making it difficult to follow and, according to some sources, can be buggy too.

## Using Other Toolchains

Integrated IDEs are great but they hide much of what is going on and can lead to bloated firmware. More control and a greater choice of editors and the toolchain require a lot more investment. More than just investment, it requires a choice about what sort of Embedded programmer to be.

## When the Chip hangs…

This was really painful for me because I couldn’t follow these instructions: use the ST supplied Windows [ST-Link Utility](http://www.st.com/content/st_com/en/products/embedded-software/development-tool-software/stsw-link004.html). Select menu item Target, Settings. Then pick *Connect Under Reset* (probably currently showing *Normal*) in the **Mode** box.
