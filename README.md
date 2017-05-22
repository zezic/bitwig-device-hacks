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

Currently, this project is undergoing massive rewrite. Stay tuned.

```
usage: builder.py [-h] [-C] device

Bitwig device multitool

positional arguments:
  device      path to device

optional arguments:
  -h, --help  show this help message and exit
  -C          clean up the device data
```


## Contacts

Style Mistake <[stylemistake@gmail.com]>

[stylemistake.com]: http://stylemistake.com
[stylemistake@gmail.com]: mailto:stylemistake@gmail.com
