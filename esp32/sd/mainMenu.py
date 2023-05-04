import ION

#create instance tft for display and touch screen
tft=ION.tft_init()
i2c = ION.I2C_init()
mouse = ION.touch()

#variables
radiusButton=0
timer=0
fade=$010101

#color set
c_font=$c9c9c9
c_button=$2f2f2f
c_background=$000000
tft.set_bg = c_button

while 1:
    #shapes
    tft.clear(c_background)
    tft.circle(160,230,20,c_button,c_button)
    tft.roundrect(110,105,100,20,5,c_button,c_button-fade)

    #text
    tft.text(tft.CENTER,222,"Tap",fade)
    tft.text(tft.CENTER,110,"11:20",fade)

    #mouse 
    mouse.update()
    
    #fadeTransition
    if (sqrt(power(mouse.x/*button_x*/-(room_width/2),2)+power(mouse.y-(room_height-10),2))<=20):
        if fade!= c_button:
            fade-=$010101
            radiusButton+=20
    else:
        radiusButton=20
        fade=c_button

#End Transition Screen
#if radButton>=300
#    showApps

#Show Apps
