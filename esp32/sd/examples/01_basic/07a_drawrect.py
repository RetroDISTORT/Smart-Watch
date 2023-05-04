# drawRect can be used to draw rectangle (filled or not)
#   with border of different color (and tickness).
#
#
from ili9341.lcd import *

l = LCD(baud = 21000000 ) # step down the SPI bus speed to 21 MHz may be opportune when using 150+ mm wires

# drawRect syntax is
#    drawRect( x, y, width, height, color, border=1, infill=None)
# with the following parameters
#  * x, y - coordonate of the top,left corner.
#  * width, height - width and height of the rectangle
#  * color - color of the rectangle's border. A (r,g,b) tuple following the RGB565 coding.
#  * border - Tickness of the border
#  * infill - filling color for the rectangle (if any filling required)
l.drawRect(5, 5, 53, 310, BLUE, border = 10, infill = ORANGE)
l.drawRect(100, 100, 50, 50, RED, border = 3, infill = GREEN)
