# test of printing multiple fonts to the ILI9341 on an M5Stack using H/W SP
# MIT License; Copyright (c) 2017 Jeffrey N. Magee

from ili934xnew import ILI9341, color565
from machine import Pin, SPI
import m5stack
import tt14
import glcdfont
import tt14
import tt24
import tt32

fonts = [glcdfont,tt14,tt24,tt32]

text = 'Now is the time for all good men to come to the aid of the party.'

power = Pin(5, Pin.OUT)
power.value(1)

spi = SPI(
    2,
    baudrate=40000000,
    miso=Pin(19),
    mosi=Pin(23),
    sck=Pin(18))

display = ILI9341(
    spi,
    cs=Pin(4),
    dc=Pin(2),
    rst=Pin(32))
display.erase()
display.set_pos(0,0)
for ff in fonts:
    display.set_font(ff)
    display.print(text)


