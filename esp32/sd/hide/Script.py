from machine import Pin
from time import sleep

led = Pin(5,Pin.OUT)

def flash():
    led.value(not led.value())
    sleep(0.5)
    led.value(not led.value())
    print("Finished flash")
    
print("Finished import")
