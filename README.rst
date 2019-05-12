=============
Lora for TTGO
=============


https://photos.app.goo.gl/cYgStJuGbR7BfsJC9

Checkout the "working" tag which is the last working version.

NOTE
====

This repo is in rough shape, and I haven't had any time to show it some love.


Motivation
==========

Wei1234c did most of the legwork originally on this project here:

https://github.com/Wei1234c/SX127x_driver_for_MicroPython_on_ESP8266

I found it hard to use to do what I needed to do with it, so I am in the process of refactoring it for my purposes.


How to Build
============

For the TTGO module, do the following.

1.  Clone the micropython repo.

2.  Link src/examples and src/sx127x directories into the ports/esp32/modules directory.

3.  Also link drivers/display (from micropython) into the ports/esp32/modules directory.

4.  Follow the micropython instructions for building the esp32 port.

5.  Flash to a TTGO Module

6.  Connect to REPL for the TTGO and run examples.duplex.test.main()

Note: As of right now, you may need to run this twice.  I believe there's a weird import error of some kind going on.
