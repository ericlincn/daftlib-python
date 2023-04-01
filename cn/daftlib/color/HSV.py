from cn.daftlib.color.IColor import IColor

class HSV(IColor):

    _h:float # Hue
    _s:float # Saturation
    _v:float # Brightness
    _r:int
    _g:int
    _b:int
    
    def __init__(self, h:float = 0.0, s:float = 1.0, v:float = 1.0) -> None:
        self._h = h
        self._s = s
        self._v = v

    @property
    def value(self, ) -> int:
        self.__updateHSVtoRGB()
        return self._r << 16 | self._g << 8 | self._b
    
    @value.setter
    def value(self, value:int) -> None:
        self._r = value >> 16
        self._g = (value & 0x00ff00) >> 8
        self._b = value & 0x0000ff
        self.__updateRGBtoHSV()

    # The value of Hue, like a angle in a color wheel( 0~360 ).<br/>
    # 0 is red, 120 is green、240 is blue.
    @property
    def h(self) -> float:
        return self._h
    
    @h.setter
    def h(self, value:float) -> None:
        self._h = value
    
    # The value of Saturation.<br/>
    # Between 0.0 ~ 1.0 , Default is 1.
    @property
    def s(self) -> float:
        return self._s
    
    @s.setter
    def s(self, value:float) -> None:
        self._s = max(0.0, min(1.0, value))
    
    # The value of Brightness.<br/>
    # Between 0.0 ~ 1.0 , Default is 1.
    @property
    def v(self) -> float:
        return self._v
    
    @v.setter
    def v(self, value:float) -> None:
        self._v = max(0.0, min(1.0, value))
    
    # Convert HSV to RGB
    def __updateHSVtoRGB(self) -> None:
        if self._s > 0:
            # h:float = ((self._h < 0) ? self._h % 360 + 360 : self._h % 360) / 60
            h = ((self._h % 360 + 360) if self._h < 0 else self._h % 360) / 60.0

            if h < 1:
                self._r = round(255 * self._v)
                self._g = round(255 * self._v * (1 - self._s * (1 - h)))
                self._b = round(255 * self._v * (1 - self._s))
            
            elif h < 2:
                self._r = round(255 * self._v * (1 - self._s * (h - 1)))
                self._g = round(255 * self._v)
                self._b = round(255 * self._v * (1 - self._s))
            
            elif h < 3:
                self._r = round(255 * self._v * (1 - self._s))
                self._g = round(255 * self._v)
                self._b = round(255 * self._v * (1 - self._s * (3 - h)))
            
            elif h < 4:
                self._r = round(255 * self._v * (1 - self._s))
                self._g = round(255 * self._v * (1 - self._s * (h - 3)))
                self._b = round(255 * self._v)
            
            elif h < 5:
                self._r = round(255 * self._v * (1 - self._s * (5 - h)))
                self._g = round(255 * self._v * (1 - self._s))
                self._b = round(255 * self._v)
            
            else:
                self._r = round(255 * self._v)
                self._g = round(255 * self._v * (1 - self._s))
                self._b = round(255 * self._v * (1 - self._s * (h - 5)))

        else:
            self._r = self._g = self._b = round(255 * self._v)


    # Convert RGB to HSV
    def __updateRGBtoHSV(self) -> None:
        if self._r != self._g or self._r != self._b:
            if self._g > self._b:
                if self._r > self._g:
                # r>g>b
                    self._v = self._r / 255
                    self._s = (self._r - self._b) / self._r
                    self._h = 60 * (self._g - self._b) / (self._r - self._b)
                
                elif self._r < self._b:
                # g>b>r
                    self._v = self._g / 255
                    self._s = (self._g - self._r) / self._g
                    self._h = 60 * (self._b - self._r) / (self._g - self._r) + 120
                
                else:
                # g=>r=>b
                    self._v = self._g / 255
                    self._s = (self._g - self._b) / self._g
                    self._h = 60 * (self._b - self._r) / (self._g - self._b) + 120
                
            else:
                if self._r > self._b:
                #  r>b=>g
                    self._v = self._r / 255
                    self._s = (self._r - self._g) / self._r
                    self._h = 60 * (self._g - self._b) / (self._r - self._g)
                    if self._h < 0:
                        self._h += 360
                
                elif self._r < self._g:
                # b=>g>r
                    self._v = self._b / 255
                    self._s = (self._b - self._r) / self._b
                    self._h = 60 * (self._r - self._g) / (self._b - self._r) + 240
                
                else:
                # b=>r=>g
                    self._v = self._b / 255
                    self._s = (self._b - self._g) / self._b
                    self._h = 60 * (self._r - self._g) / (self._b - self._g) + 240

        else:
            self._h = self._s = 0
            self._v = self._r / 255