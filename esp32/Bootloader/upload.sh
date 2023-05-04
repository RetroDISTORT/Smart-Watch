#! /bin/sh
esptool.py --port /dev/ttyUSB0 erase_flash
esptool.py --port /dev/ttyUSB0 write_flash 0x1000 esp32spiram-20210623-v1.16.bin
