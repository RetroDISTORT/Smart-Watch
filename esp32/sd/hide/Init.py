import machine
import os

def boot():
	backlight = Pin(5,Pin.OUT)
    backlight.value(not backlight.value())
    sleep(0.1)
    led.value(not led.value())
    print("Finished flash")
    
def mountSD():
	sd = machine.SDCard(slot=2, width=1, cd=None, wp=None, sck=18, miso=19, mosi=23, cs=15)
	os.mount(sd,'/sd')

print("Finished import")
