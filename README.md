# Bitwig Device Hacks

If you're feeling, that Bitwig modulation system is not complete, you're not
alone. With this tool you will be able to modify the Math device and create
your own.

Bitwig Studio 2.0 has a DSP language, called "Nitro", which Bitwig developers
use to power their modulation system and their new Amp device. Source code of
these devices is stored in plain text, and compiled at runtime.

This language doesn't have an open API yet, but who needs API when it's
quite easy to hack yourself in?

[Sample code in Nitro](https://p.smx.lt/CKtksmU)


## Description

For demonstration purposes, this repository contains a `MathX` modulator,
which has different operation modes:

- `DIV` - Division (`a/(b×10)`)
- `SIG` - Sign of the signal (outputs -1 or +1)
- `POW` - Power function (`a^(b×10)`)
- `LOG` - Natural logarithm (`ln(a)`)
- `SIN` - Sine function (`sin(a×π)`)
- `EMA` - Exponential moving average (`a` is the input, `b` is the smoothing coefficient)

It's located in `resources/MathX.bwmodulator`, and to install it, you need to
place it into your Bitwig installation folder at
`<Bitwig Studio>/Library/modulators/` and restart the Bitwig Studio.


## Build process

- `resources/Math.nitro.c` - source code of the math device
- `resources/Math.mapping.txt` - function name mappings

To build a MathX device, run `python repack.py`.


## Contacts

Style Mistake <[stylemistake@gmail.com]>

[stylemistake.com]: http://stylemistake.com
[stylemistake@gmail.com]: mailto:stylemistake@gmail.com
