#This file boots the SD Card and runs init.py
#import machine, os
#HSPI
SD = machine.SDCard(slot=1, sck = 14, miso = 2, mosi = 15, cs = 13, freq = 20000000)
#VSPI
#SD = machine.SDCard(slot=2, sck = 18, miso = 19, mosi = 23, cs = 15, freq = 20000000)
#uos.mount(SD,"/sd")
#uos.chdir("/sd")
#import init

#LOBO

#import machine, os, uos
#uos.sdconfig(uos.SDMODE_SPI, clk=18, miso=19, mosi=23, cs=15)
#os.mountsd(1)

#import init

