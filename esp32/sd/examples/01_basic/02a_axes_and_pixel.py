# In this sample we will:
# * See the screen axes (in related image)
# * Draw a single pixel
#
from ili9341.lcd import *

l = LCD(baud = 21000000) # step down the SPI bus speed to 21 MHz may be opportune when using 150+ mm wires                                                    
l.drawPixel(80, 130, RED) # x=80, y=130
