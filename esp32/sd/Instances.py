'''
* Instances
* Author: Daniel Garcia
* Date: October 14, 2020
*
* This code is used for Gui and onscreen instances
* It works by executing each instance's draw and step events
* 
*
*
'''

class button:
    def __init__(device,x,y,w,h,text,c_primary,c_secondary,c_text):
        self.device=device
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.c_primary
        self.c_secondary
        self.c_text

    def update(self):
        draw();
        touch();

    def draw(self):
        device.display.screen.rect(x,y,w,h,c_primary,c_secondary)
        device.display.screen.text(x,y,w/2,h/2,c_text)

    def touch(self,function):
        device.touch.update()
        if device.touch.x>x and device.touch.x<x+w and device.touch.y>y and device.touch.y<y+h:
            print("touching me")
            function

    def 
