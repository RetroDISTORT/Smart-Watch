'''
* ION
* Author: Daniel Garcia
* Date: Aug 16, 2020
*  
* Code specifically writen for the ESP32 - String I/ON
* This code has the whole funcionality of all the external hardware in the device.
* Most modules were taken from the Loboris Micropython Firmware Build.
* Informaion for these modules can be found at:
*      Loboris Wiki: https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/
*
'''

import machine, time, struct, display
from micropython import const

class Device:
    def __init__(self):
        self.display = Display()
        self.led = LED()
        self.serial = Serial()
        self.touch = Touch(self.serial.i2c)
        self.buttons = Buttons()
        self.server = Server()
        
        #self.sensors = Sensors(self.serial.i2c)
        #self.barometer = ION.barometer()
        #self.lightSensor = ION.lightSensor()
        #self.heartRateMonitor = ION.heartRateMonitor_init()
        
        #self.i2s = ION.i2s_init()
        #self.mic = ION.mic_init()
        #self.speaker = ION.speaker_init()
        #self.battery = ION.battery_init()
        #self.haptic = ION.haptic_init()
        
        #self.infrared = ION.infrared()

class Display:
    def __init__(self):
        # Initial Setup
        self.reset = machine.Pin(32, machine.Pin.OUT)
        self.backlight = machine.PWM(5)
        self.backlight.freq(500)
        self.backlight.duty(50)

        # Define ILI9341 command constants
        _RDDSDR    = const(0x0f) # Read Display Self-Diagnostic Result
        _SLPOUT    = const(0x11) # Sleep Out
        _GAMSET    = const(0x26) # Gamma Set
        _DISPOFF   = const(0x28) # Display Off
        _DISPON    = const(0x29) # Display On
        _CASET     = const(0x2a) # Column Address Set
        _PASET     = const(0x2b) # Page Address Set
        _RAMWR     = const(0x2c) # Memory Write
        _RAMRD     = const(0x2e) # Memory Read
        _MADCTL    = const(0x36) # Memory Access Control
        _VSCRSADD  = const(0x37) # Vertical Scrolling Start Address
        _PIXSET    = const(0x3a) # Pixel Format Set
        _PWCTRLA   = const(0xcb) # Power Control A
        _PWCRTLB   = const(0xcf) # Power Control B
        _DTCTRLA   = const(0xe8) # Driver Timing Control A
        _DTCTRLB   = const(0xea) # Driver Timing Control B
        _PWRONCTRL = const(0xed) # Power on Sequence Control
        _PRCTRL    = const(0xf7) # Pump Ratio Control
        _PWCTRL1   = const(0xc0) # Power Control 1
        _PWCTRL2   = const(0xc1) # Power Control 2
        _VMCTRL1   = const(0xc5) # VCOM Control 1
        _VMCTRL2   = const(0xc7) # VCOM Control 2
        _FRMCTR1   = const(0xb1) # Frame Rate Control 1
        _DISCTRL   = const(0xb6) # Display Function Control
        _ENA3G     = const(0xf2) # Enable 3G
        _PGAMCTRL  = const(0xe0) # Positive Gamma Control
        _NGAMCTRL  = const(0xe1) # Negative Gamma Control

        # Generating instance
        self.screen = display.TFT()
        self.screen.init(self.screen.ILI9341, width=240, height=320, miso=19, mosi=23, clk=18, cs=22, dc=2, speed=40000000, bgr=True, color_bits=16)

        # Reset
        self.reset.value(0)
        time.sleep_ms(120)
        self.reset.value(1)

        # Send initialization commands
        for command, data in (
                (_RDDSDR,    b"\x03\x80\x02"),
                (_PWCRTLB,   b"\x00\xc1\x30"),
                (_PWRONCTRL, b"\x64\x03\x12\x81"),
                (_DTCTRLA,   b"\x85\x00\x78"),
                (_PWCTRLA,   b"\x39\x2c\x00\x34\x02"),
                (_PRCTRL,    b"\x20"),
                (_DTCTRLB,   b"\x00\x00"),
                (_PWCTRL1,   b"\x23"),
                (_PWCTRL2,   b"\x10"),
                (_VMCTRL1,   b"\x3e\x28"),
                (_VMCTRL2,   b"\x86"),
                (_MADCTL,    b"\x48"),
                #(_MADCTL, b"\x08"),
                (_PIXSET,    b"\x55"),
                (_FRMCTR1,   b"\x00\x18"),
                (_DISCTRL,   b"\x08\x82\x27"),
                (_ENA3G,     b"\x00"),
                (_GAMSET,    b"\x01"),
                (_PGAMCTRL,  b"\x0f\x31\x2b\x0c\x0e\x08\x4e\xf1\x37\x07\x10\x03\x0e\x09\x00"),
                (_NGAMCTRL,  b"\x00\x0e\x14\x03\x11\x07\x31\xc1\x48\x08\x0f\x0c\x31\x36\x0f")):
            self.screen.tft_writecmddata(command, data)
            self.screen.tft_writecmd(_SLPOUT)
            time.sleep_ms(120)
            self.screen.tft_writecmd(_DISPON)
            self.backlight.duty(100)

            #return generated instance
            #return(disp)

#GUI
'''class Gui:
    def __init__(self,display,touch,radius,color,fill,text):
        gui.instances = []

    def new(self):

    def touched(self):
        self.touch.update()
        return all(self.touch.x>self.x,self.touch.y>self.y,self.touch.x<(self.x+self.width),self.touch.y<(self.y+self.height))
        
    def roundButton(self):
        self.display.roundrect(x,y,width,height,color=self.color,fill=self.fill)

    def slider(self,slider,x,y,width,height,text,scroll,selected,radius,fill,outline):
        self.display=display
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.text=text
        self.scroll=scroll
        self.selected=selected
        self.radius=radius
        self.fill=fill
        self.outline=outline
        self.display.roundrect(slider.x,slider.y,slider.width,slider.height,slider.radius,slider.outline)
        self.display.line(slider.x,slider.y+(slider.height/2),slider.x+slider.width,slider.y+(slider.height/2),slider.outline)
'''     
        
"""
class option:
    def __Init__(self,x,y,width,height,text):

class list:
    def __Init__(self,x,y,width,height,text):

class text:
    def __Init__(self,x,y,width,height,text):

class input:
    def __init__(self,x,y,width,height,text):
"""

#LEDs
from machine import Pin

class LED:
    def __init__(self):
        self.enable = Pin(21,Pin.OUT)
        self.enable.value(1)
        self.pixel  = machine.Neopixel(0,3,1)

#Buttons
from machine import Pin
from machine import ADC
from time    import sleep

def button_callback(value):
    adc = ADC(Pin(36)) #setup for Analog Read
    adc.atten(ADC.ATTN_11DB) #setup for Analog Range
    
    if adc.read()>2500:
        print("Entering Deepsleep...")
        while adc.read()>1000:
            pass
        machine.deepsleep()
        
    if adc.read()>2000:
        print("Starting Reset...")
        while adc.read()>1000:
            pass
        machine.reset()

class Buttons:
    def __init__(self):
        #button = Pin(36, Pin.IN) #setup for Deepsleep

        rtc = machine.RTC()
        rtc.wake_on_ext0(Pin(36),Pin(36).IRQ_RISING) #wakeup signal Loboris
        button = machine.Pin(36,handler=button_callback,trigger=Pin(36).IRQ_RISING)
        #esp32.wake_on_ext0(pin = button, level = esp32.WAKEUP_ANY_HIGH) #setup wakeup signal
        #p0.irq(trigger=button.IRQ_FALLING, handler=callback)
    
        
#Generates serial buses using the default pins
class Serial:
    def  __init__ (self):
        self.i2c = machine.I2C(scl=machine.Pin(14),sda=machine.Pin(27))
        #self.spi =
        #self.uart =
        #self.uart = UART(1, tx=12, rx=15, baudrate=9600)

'''
#MPU
import utime
from machine import I2C, Pin
from mpu9250 import MPU9250

class Sensors:
    def __init__(self,i2c):
        self.I2C=i2c 
        mpu = MPU9250(self.I2C) #https://pypi.org/project/micropython-mpu9250/
        #lightSensor = 
        #barometer = 
'''       
        
''' WORK IN PROGRESS
#TSL2561
#import struct
_TSL256X_I2C_ADDR = 0x39

_TSL256X_REG_CONTROL = const(0x00)
_TSL256X_REG_TIMING = const(0x01)
_TSL256X_REG_THRESHOLD_LL = const(0x02)
_TSL256X_REG_THRESHOLD_LH = const(0x03)
_TSL256X_REG_THRESHOLD_HL = const(0x04)
_TSL256X_REG_THRESHOLD_HH = const(0x05)
_TSL256X_REG_INTERRUPT = const(0x06)
_TSL256X_REG_ID = const(0x0A)
_TSL256X_REG_DATA0_L = const(0x0C)
_TSL256X_REG_DATA0_H = const(0x0D)
_TSL256X_REG_DATA1_L = const(0x0E)
_TSL256X_REG_DATA1_H = const(0x0F)

class TSL2561:
    def __init__(self, i2c, address = _TSL256X_I2C_ADDR):
        self.buf = bytearray(3)
        self.addr = address
        self.I2C = i2c

    def chip_id(self):
        #chip_id=
'''

#FT6206
import struct
_FT6206_I2C_ADDR_ = 0x38

_FT6206_REG_DATA       = const(0x00)      #
_FT6206_REG_GEST_ID    = const(0x01)   #GESTURE ID
_FT6206_REG_TD_STATUS  = const(0x02) #NUMBER OF THOUCHPOINTS
_FT6206_REG_TH_GROUP   = const(0x80)  #THRESHOLD REG
_FT6206_REG_POINTRATE  = const(0x88)
_FT6206_REG_LIBH       = const(0xA1)
_FT6206_REG_LIBL       = const(0xA2)
_FT6206_REG_CHIPID     = const(0xA3)
_FT6206_REG_FIRMVERS   = const(0xA6)
_FT6206_REG_VENDID     = const(0xA8)
_FT6206_REG_RELEASE    = const(0xAF)
    
chip = None

class Touch:
    def __init__(self,i2c,address = _FT6206_I2C_ADDR_, dev_Mode=False):
        self.I2C         = i2c
        self.touchPoints = 0
        self.rotation    = 0

        self.x  = 0
        self.y  = 0

        self.x1 = 0
        self.y1 = 0
        self.w1 = 0
        self.a1 = 0

        self.x2 = 0
        self.y2 = 0
        self.w2 = 0
        self.a2 = 0

        self.gesture = 0

        chip_data = self.I2C.readfrom_mem(_FT6206_I2C_ADDR_, _FT6206_REG_LIBH, 8)
        lib_ver, chip_id, _, _, frim_id, _, vend_id = struct.unpack(">HBBBBBB", chip_data)

        if vend_id != 0x11:
            raise RuntimeError("Did not find FT chip. Chip is in Hibernation mode or not connected.")
            

        chip = "UNKNOWN"
        if chip_id == 0x06:
            self.chip = "FT6206"

        if dev_Mode:
            print("Library vers %04X" % lib_ver)
            print("Firmware ID %02X" % firm_id)
            print("Point rate %d Hz" % self.i2c.readfrom_mem(_FT6206_REG_POINTRATE, 1)[0])
            print("Thresh %d" % self.i2c.readfrom_mem(_FT6206_REG_THRESHHOLD, 1)[0])
    
    def touched(self):
        return self.I2C.readfrom_mem(_FT6206_I2C_ADDR_, _FT6206_REG_TD_STATUS, 1)[0]

    def rotate(self,rotation):
        if all(rotation>3,rotation<0):
            return "invalid input"
        else:
            self.rotation=rotation
            return rotation

    def set_threshold(self,threshold):
        buf = char(threshold,16)
        self.I2C.writeto_mem(_FT6206_I2C_ADDR_,_FT6206_REG_TH_GROUP,threshold)

    def get_threshhold(self):
        return self.I2C.readfrom_mem(_FT6206_I2C_ADDR_,_FT6206_REG_TH_GROUP,1)

    def get_gesture(self):
        return self.I2C.readfrom_mem(_FT6206_I2C_ADDR_,_FT6206_REG_GEST_ID,1)

    def update(self):
        touchpoints = []
        data = self.I2C.readfrom_mem(_FT6206_I2C_ADDR_,0x00,32)
        
        for i in range(2):
            point_data = data[i * 6 + 3 : i * 6 + 9]
            if all([i == 0xFF for i in point_data]):
                continue
            # print([hex(i) for i in point_data])
            x, y, weight, misc = struct.unpack(">HHBB", point_data)
            # print(x, y, weight, misc)
            touch_id  = y >> 12
            x &= 0xFFF
            y &= 0xFFF

            #rotation
            if self.rotation == 1:
                hold = x
                x    = 240-hold
            if self.rotation == 2:
                hold = x
                x    = y
                y    = hold
            if self.rotation == 3:
                hold=y
                y=320-hold
            
            point = {"x": x, "y": y, "id": touch_id}
            touchpoints.append(point)
            if i == 0:
                self.x  = x
                self.y  = y
                self.x1 = x
                self.y1 = y
            else:
                self.x2 = x
                self.y2 = y

        return touchpoints

import machine, network, utime
class Server:
    def __init__(self):
        self.name= "Network"

    def startup(self):
        print("Starting WiFi ...")
        sta_if = network.WLAN(network.AP_IF)
        sta_if.active(True)
        utime.sleep_ms(1000)
        print(sta_if.ifconfig())
        network.telnet.start()
        utime.sleep_ms(1000)
        print ("Telnet Started ",network.telnet.status())
        network.ftp.start()
        utime.sleep_ms(1000)
        print ("FTP Started ",network.ftp.status())
        print ("Wifi Network: ESP_XXXXX")
        print ("Remote Hoste Name or IP: 192.168.4.1  Port: 23")
