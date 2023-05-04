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
tft.init(tft.ILI9341, width=240, height=320, miso=19, mosi=23, clk=18, cs=4, dc=2, bgr=True, color_bits=16, invrot=3)

# Initialize the display
tft_init(tft)

# We can naw use all display commands


# fonts used in this demo
fontnames = (
    tft.FONT_Default,
    tft.FONT_7seg,
    tft.FONT_Ubuntu,
    tft.FONT_Comic,
    tft.FONT_Tooney,
    tft.FONT_Minya
)


# print display header
#----------------------
def header(tx, setclip):
    # adjust screen dimensions (depends on used display and orientation)
    global maxx, maxy, miny

    maxx, maxy = tft.screensize()
    tft.clear()
    if maxx < 240:
        tft.font(tft.FONT_Small, rotate=0)
    else:
        tft.font(tft.FONT_Default, rotate=0)
    _,miny = tft.fontSize()
    miny += 5
    tft.rect(0, 0, maxx-1, miny-1, tft.OLIVE, tft.DARKGREY)
    tft.text(tft.CENTER, 2, tx, tft.CYAN, transparent=True)

    if setclip:
        tft.setwin(0, miny, maxx, maxy)

# Display some fonts
#-------------------
def dispFont(sec=5):
    header("DISPLAY FONTS", False)

    if maxx < 240:
        tx = "MicroPython"
    else:
        tx = "Hi from MicroPython"
    starty = miny + 4

    n = time.time() + sec
    while time.time() < n:
        y = starty
        x = 0
        i = 0
        while y < maxy:
            if i == 0: 
                x = 0
            elif i == 1:
                x = tft.CENTER
            elif i == 2:
                x = tft.RIGHT
            i = i + 1
            if i > 2:
                i = 0
            
            for font in fontnames:
                if font == tft.FONT_7seg:
                    tft.font(font)
                    tft.text(x,y,"-12.45/",machine.random(0xFFFFFF))
                else:
                    tft.font(font)
                    tft.text(x,y,tx, machine.random(0xFFFFFF))
                _,fsz = tft.fontSize()
                y = y + 2 + fsz
                if y > (maxy-fsz):
                    y = maxy
        if touched():
            break

# Display random fonts
#------------------------------
def fontDemo(sec=5, rot=False):
    tx = "FONTS"
    if rot:
        tx = "ROTATED " + tx
    header(tx, True)

    tx = "ESP32-MicrpPython"
    n = time.time() + sec
    while time.time() < n:
        frot = 0
        if rot:
            frot = math.floor(machine.random(359)/5)*5
        for font in fontnames:
            if (not rot) or (font != tft.FONT_7seg):
                x = machine.random(maxx-8)
                if font != tft.FONT_7seg:
                    tft.font(font, rotate=frot)
                    _,fsz = tft.fontSize()
                    y = machine.random(miny, maxy-fsz)
                    tft.text(x,y,tx, machine.random(0xFFFFFF))
                else:
                    l = machine.random(6,12)
                    w = machine.random(1,l // 3)
                    tft.font(font, rotate=frot, dist=l, width=w)
                    _,fsz = tft.fontSize()
                    y = machine.random(miny, maxy-fsz)
                    tft.text(x,y,"-12.45/", machine.random(0xFFFFFF))
        if touched():
            break
    tft.resetwin()

# Display random lines
#-------------------
def lineDemo(sec=5):
    header("LINE DEMO", True)

    n = time.time() + sec
    while time.time() < n:
        x1 = machine.random(maxx-4)
        y1 = machine.random(miny, maxy-4)
        x2 = machine.random(maxx-1)
        y2 = machine.random(miny, maxy-1)
        color = machine.random(0xFFFFFF)
        tft.line(x1,y1,x2,y2,color)
        if touched():
            break
    tft.resetwin()

# Display random circles
#----------------------------------
def circleDemo(sec=5,dofill=False):
    tx = "CIRCLE"
    if dofill:
        tx = "FILLED " + tx
    header(tx, True)

    n = time.time() + sec
    while time.time() < n:
        color = machine.random(0xFFFFFF)
        fill = machine.random(0xFFFFFF)
        x = machine.random(4, maxx-2)
        y = machine.random(miny+2, maxy-2)
        if x < y:
            r = machine.random(2, x)
        else:
            r = machine.random(2, y)
        if dofill:
            tft.circle(x,y,r,color,fill)
        else:
            tft.circle(x,y,r,color)
        if touched():
            break
    tft.resetwin()

#------------------
def circleSimple():
    tx = "CIRCLE"
    header(tx, True)

    x = 110
    y = 160
    r = 110
    z = 0
    while z < 12:
        color = machine.random(0xFFFFFF)
        fill = machine.random(0xFFFFFF)
        tft.circle(x,y,r,color,fill)
        r -= 10
        x += 10
        z += 1

# Display random ellipses
#-----------------------------------
def ellipseDemo(sec=5,dofill=False):
    tx = "ELLIPSE"
    if dofill:
        tx = "FILLED " + tx
    header(tx, True)

    n = time.time() + sec
    while time.time() < n:
        x = machine.random(4, maxx-2)
        y = machine.random(miny+2, maxy-2)
        if x < y:
            rx = machine.random(2, x)
        else:
            rx = machine.random(2, y)
        if x < y:
            ry = machine.random(2, x)
        else:
            ry = machine.random(2, y)
        color = machine.random(0xFFFFFF)
        if dofill:
            fill = machine.random(0xFFFFFF)
            tft.ellipse(x,y,rx,ry,15, color,fill)
        else:
            tft.ellipse(x,y,rx,ry,15,color)
        if touched():
            break
    tft.resetwin()

# Display random rectangles
#---------------------------------
def rectDemo(sec=5, dofill=False):
    tx = "RECTANGLE"
    if dofill:
        tx = "FILLED " + tx
    header(tx, True)

    n = time.time() + sec
    while time.time() < n:
        x = machine.random(4, maxx-2)
        y = machine.random(miny, maxy-2)
        w = machine.random(2, maxx-x)
        h = machine.random(2, maxy-y)
        color = machine.random(0xFFFFFF)
        if dofill:
            fill = machine.random(0xFFFFFF)
            tft.rect(x,y,w,h,color,fill)
        else:
            tft.rect(x,y,w,h,color)
        if touched():
            break
    tft.resetwin()

# Display random rounded rectangles
#--------------------------------------
def roundrectDemo(sec=5, dofill=False):
    tx = "ROUND RECT"
    if dofill:
        tx = "FILLED " + tx
    header(tx, True)

    n = time.time() + sec
    while time.time() < n:
        x = machine.random(2, maxx-18)
        y = machine.random(miny, maxy-18)
        w = machine.random(12, maxx-x)
        h = machine.random(12, maxy-y)
        if w > h:
            r = machine.random(2, h // 2)
        else:
            r = machine.random(2, w // 2)
        color = machine.random(0xFFFFFF)
        if dofill:
            fill = machine.random(0xFFFFFF)
            tft.roundrect(x,y,w,h,r,color,fill)
        else:
            tft.roundrect(x,y,w,h,r,color)
        if touched():
            break
    tft.resetwin()