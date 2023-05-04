#import ION

#Buttons
from machine import Pin
from machine import ADC
from time import sleep

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


