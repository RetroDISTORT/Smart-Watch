from os import listdir
from utime import sleep, ticks_ms

from lcd import LCD, Chars, ILI, imgdir, cachedir, imgcachepath
from colors import *

class BaseTests(LCD, Chars):

    def __init__(self, **kwargs):
        super(BaseTests, self).__init__(**kwargs)

    def charsTest(self, color, font = None, scale = 1):
        ch = self.initCh(color = color, font = font, scale = scale)
        scale = 3 if scale >= 3 else scale
        x = y = 5
        font = ch._font
        fwidth = font['width']
        for i in range(33, 256):
            try:
                chrwidth = len(font[i])
            except KeyError:
                continue
            ch.printChar(chr(i), x, y, scale=scale)
            x += self._asm_get_charpos(chrwidth, scale, 3)
            if x > (self.curWidth - fwidth * scale):
                x = 10
                y = self._asm_get_charpos(font['height'], scale, y)

    def renderImageTest(self, cached = True, path = imgdir,
                        cpath = cachedir, delay = 0, bgcolor = BLACK):
        starttime = ticks_ms() // 1000
        cachelist = listdir(imgcachepath)
        print(cachedir + 'd ' + imgdir + ':', cachelist)
        for image in listdir(path):
            if image != cpath and image.endswith('bmp'):
                self.renderBmp(image, cached = cached, bgcolor = bgcolor)
                if delay:
                    sleep(delay / 1000)
        return (ticks_ms() // 1000 - starttime) / 1000

    def charsBGcolorTest(self, color = BLACK, font = None, scale = 1):
        if font is None:
            from exceptions import NoneTypeFont
            raise NoneTypeFont
        self.portrait = True
        s = self.initCh(font = font, color = color, scale = scale)
        x = self.curWidth // 2 - (s.font['width'] // 2) * scale
        y = self.curHeight // 2 - (s.font['height'] // 2) * scale
        colors = [BLACK, NAVY, DARKGREEN, DARKCYAN, MAROON, PURPLE, OLIVE,
                LIGHTGREY, DARKGREY, BLUE, GREEN, CYAN, RED, MAGENTA, YELLOW,
                WHITE, ORANGE, GREENYELLOW]
        j = 33
        self._gcCollect()
        for i in range((255 - 33) // 16):
            for clr in colors:
                if isinstance(color, tuple) and color != clr:
                    self.fillMonocolor(clr)
                    s.printChar(chr(j), x, y)
                    j += 1
                    sleep(0.1)
        self._gcCollect()

    def rgbInfillTest(self):
        self.portrait = True
        red = green = blue = 0
        for i in range(2 ** 16):
            if red > 31:
                red = 0
            if green > 63:
                green = 0
            self.fillMonocolor((red, green, blue))
            red += 1
            if red == 32:
                green += 1
            if green == 64:
                blue += 1
                print(i, 'blue is', blue)

    def rectInfillTest(self, portrait = True, border = 1):
        strobj = self.initCh(font = 'Arial_14', color = BLACK)
        prevportr = self.portrait
        if prevportr != portrait:
            self.portrait = portrait
        height = self.curHeight
        width = self.curWidth
        self.drawRect(0, 0, width, 30, DARKCYAN, border = 0)
        self.drawHline(0, 29, width, BLACK, width = 1)
        string = 'height:'
        self.label(5, 2, BLACK, LIGHTGREY, string, strobj = strobj)
        self._gcCollect()
        for i in range(1 + border * 2, height - 40):
            string = '{0}px'.format(i)
            self.drawRect(120, 0, 50, 28, DARKCYAN, border = 0)
            self.label(76, 2, BLACK, LIGHTGREY, string, strobj = strobj)
            self.drawRect(0, 30, width, height-30, YELLOW, border = 0)
            self.drawRect(5, 35, width-10, i, BLUE, infill = GREEN, border = border)
            self._gcCollect()
            sleep(0.5)
        self.portrait = prevportr
