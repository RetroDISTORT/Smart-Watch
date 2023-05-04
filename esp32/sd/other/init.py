import machine, display, time
from micropython import const

tft_rst = machine.Pin(32, machine.Pin.OUT, 1)
tft_bckl = machine.Pin(5, machine.Pin.OUT, 0)

# Define ILI9341 command constants
_RDDSDR = const(0x0f) # Read Display Self-Diagnostic Result
_SLPOUT = const(0x11) # Sleep Out
_GAMSET = const(0x26) # Gamma Set
_DISPOFF = const(0x28) # Display Off
_DISPON = const(0x29) # Display On
_CASET = const(0x2a) # Column Address Set
_PASET = const(0x2b) # Page Address Set
_RAMWR = const(0x2c) # Memory Write
_RAMRD = const(0x2e) # Memory Read
_MADCTL = const(0x36) # Memory Access Control
_VSCRSADD = const(0x37) # Vertical Scrolling Start Address
_PIXSET = const(0x3a) # Pixel Format Set
_PWCTRLA = const(0xcb) # Power Control A
_PWCRTLB = const(0xcf) # Power Control B
_DTCTRLA = const(0xe8) # Driver Timing Control A
_DTCTRLB = const(0xea) # Driver Timing Control B
_PWRONCTRL = const(0xed) # Power on Sequence Control
_PRCTRL = const(0xf7) # Pump Ratio Control
_PWCTRL1 = const(0xc0) # Power Control 1
_PWCTRL2 = const(0xc1) # Power Control 2
_VMCTRL1 = const(0xc5) # VCOM Control 1
_VMCTRL2 = const(0xc7) # VCOM Control 2
_FRMCTR1 = const(0xb1) # Frame Rate Control 1
_DISCTRL = const(0xb6) # Display Function Control
_ENA3G = const(0xf2) # Enable 3G
_PGAMCTRL = const(0xe0) # Positive Gamma Control
_NGAMCTRL = const(0xe1) # Negative Gamma Control

#------------------
def tft_init(disp):
    # Reset
    tft_rst.value(0)
    time.sleep_ms(120)
    tft_rst.value(1)

    # Send initialization commands
    for command, data in (
        (_RDDSDR, b"\x03\x80\x02"),
        (_PWCRTLB, b"\x00\xc1\x30"),
        (_PWRONCTRL, b"\x64\x03\x12\x81"),
        (_DTCTRLA, b"\x85\x00\x78"),
        (_PWCTRLA, b"\x39\x2c\x00\x34\x02"),
        (_PRCTRL, b"\x20"),
        (_DTCTRLB, b"\x00\x00"),
        (_PWCTRL1, b"\x23"),
        (_PWCTRL2, b"\x10"),
        (_VMCTRL1, b"\x3e\x28"),
        (_VMCTRL2, b"\x86"),
        (_MADCTL, b"\x48"),
        #(_MADCTL, b"\x08"),
        (_PIXSET, b"\x55"),
        (_FRMCTR1, b"\x00\x18"),
        (_DISCTRL, b"\x08\x82\x27"),
        (_ENA3G, b"\x00"),
        (_GAMSET, b"\x01"),
        (_PGAMCTRL, b"\x0f\x31\x2b\x0c\x0e\x08\x4e\xf1\x37\x07\x10\x03\x0e\x09\x00"),
        (_NGAMCTRL, b"\x00\x0e\x14\x03\x11\x07\x31\xc1\x48\x08\x0f\x0c\x31\x36\x0f")):
        disp.tft_writecmddata(command, data)
    disp.tft_writecmd(_SLPOUT)
    time.sleep_ms(120)
    disp.tft_writecmd(_DISPON)
    tft_bckl.value(1)


tft = display.TFT()

# Init display with GENERIC type, the display will not be initialized
# This, for example, works for M5Stack display
#tft.init(tft.GENERIC, width=240, height=320, miso=19, mosi=23, clk=18, cs=14, dc=27, bgr=True, color_bits=16, invrot=3)
tft.init(tft.ILI9341, width=240, height=320, miso=19, mosi=23, clk=18, cs=4, dc=2, speed=40000000, bgr=True, color_bits=16)

# Initialize the display
tft_init(tft)

# We can naw use all display commands

fontnames = (
    tft.FONT_Ubuntu
)

maxx = 240
maxy = 320
miny = 12

tft.clear(tft.BLACK)
tft.orient(tft.LANDSCAPE)

tft.circle(160,120,90,tft.WHITE,tft.BLACK)
tft.circle(75, 55,32,tft.WHITE,tft.BLACK)
tft.font(tft.FONT_Ubuntu, rotate=0)
tft.text(55, 45, "+", tft.WHITE, transparent=True)
tft.text(tft.CENTER, 120, "I/ON", tft.WHITE, transparent=True)
tft.text(tft.CENTER, 215, "Powered by: MicroPython", tft.WHITE, transparent=True)

time.sleep(1)

import mainMenu

