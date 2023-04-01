from cn.daftlib.color.IColor import IColor

class HSL(IColor):

    _h:float # Hue
    _s:float # Saturation
    _l:float # Lightness
    _r:int
    _g:int
    _b:int
    
    def __init__(self, h:float = 0.0, s:float = 1.0, l:float = 0.5) -> None:
        self._h = h
        self._s = s
        self._l = l

    @property
    def value(self) -> int:
        self.__updateHSLtoRGB()
        return self._r << 16 | self._g << 8 | self._b
    
    @value.setter
    def value(self, value:int) -> None:
        self._r = value >> 16
        self._g = (value & 0x00ff00) >> 8
        self._b = value & 0x0000ff
        self.__updateRGBtoHSL()
    
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
    
    # The value of Lightness.<br/>
    # Between 0.0 ~ 1.0 , Default is 1.
    @property
    def l(self) -> float:
        return self._l
    
    @l.setter
    def l(self, value:float) -> None:
        self._l = max(0.0, min(1.0, value))
    
    # Convert HSL to RGB
    def __updateHSLtoRGB(self) -> None:
        if self._s > 0:
            # v:Number = (_l <= 0.5) ? _l + _s * _l : _l + _s * (1 - _l)
            # p:Number = 2.0 * _l - v
            # h:Number = ((_h < 0) ? _h % 360 + 360 : _h % 360) / 60
            v:float = self._l + self._s * self._l if self._l <= 0.5 else self._l + self._s * (1 - self._l)
            p:float = 2.0 * self._l - v
            h:float = ((self._h % 360 + 360) if self._h < 0 else self._h % 360) / 60.0

            if h < 1:
                self._r = round(255 * v)
                self._g = round(255 * (p + (v - p) * h))
                self._b = round(255 * p)
            
            elif h < 2:
                self._r = round(255 * (p + (v - p) * (2 - h)))
                self._g = round(255 * v)
                self._b = round(255 * p)
            
            elif h < 3:
                self._r = round(255 * p)
                self._g = round(255 * v)
                self._b = round(255 * (p + (v - p) * (h - 2)))
            
            elif h < 4:
                self._r = round(255 * p)
                self._g = round(255 * (p + (v - p) * (4 - h)))
                self._b = round(255 * v)
            
            elif h < 5:
                self._r = round(255 * (p + (v - p) * (h - 4)))
                self._g = round(255 * p)
                self._b = round(255 * v)
            
            else:
                self._r = round(255 * v)
                self._g = round(255 * p)
                self._b = round(255 * (p + (v - p) * (6 - h)))
            
        else:
            self._r = self._g = self._b = round(255 * self._l)

    # Convert RGB to HSL
    def __updateRGBtoHSL(self) -> None:
        if self._r != self._g or self._r != self._b:
            if self._g > self._b:
                if self._r > self._g:
                    # r>g>b
                    # _l = (_r + _b)
                    # _s = (_l > 255) ? (_r - _b) / (510 - _l) : (_r - _b) / _l
                    # _h = 60 * (_g - _b) / (_r - _b)
                    self._l = (self._r + self._b)
                    self._s = (self._r - self._b) / (510 - self._l) if self._l > 255 else (self._r - self._b) / self._l
                    self._h = 60 * (self._g - self._b) / (self._r - self._b)
                
                elif self._r < self._b:
                    # g>b>r
                    # _l = (_g + _r)
                    # _s = (_l > 255) ? (_g - _r) / (510 - _l) : (_g - _r) / _l
                    # _h = 60 * (_b - _r) / (_g - _r) + 120
                    self._l = (self._g + self._r)
                    self._s = (self._g - self._r) / (510 - self._l) if self._l > 255 else (self._g - self._r) / self._l
                    self._h = 60 * (self._b - self._r) / (self._g - self._r) + 120
                
                else:
                    # g=>r=>b
                    # _l = (_g + _b)
                    # _s = (_l > 255) ? (_g - _b) / (510 - _l) : (_g - _b) / _l
                    # _h = 60 * (_b - _r) / (_g - _b) + 120
                    self._l = (self._g + self._b)
                    self._s = (self._g - self._b) / (510 - self._l) if self._l > 255 else (self._g - self._b) / self._l
                    self._h = 60 * (self._b - self._r) / (self._g - self._b) + 120
            
            else:
                if self._r > self._b:
                # r>b=>g
                    # _l = (_r + _g)
                    # _s = (_l > 255) ? (_r - _g) / (510 - _l) : (_r - _g) / _l
                    # _h = 60 * (_g - _b) / (_r - _g)
                    # if(_h < 0)
                    #     _h += 360
                    self._l = (self._r + self._g)
                    self._s = (self._r - self._g) / (510 - self._l) if self._l > 255 else (self._r - self._g) / self._l
                    self._h = 60 * (self._g - self._b) / (self._r - self._g)
                    if self._h < 0:
                        self._h += 360
                
                elif self._r < self._g:
                    # b=>g>r
                    # _l = (_b + _r)
                    # _s = (_l > 255) ? (_b - _r) / (510 - _l) : (_b - _r) / _l
                    # _h = 60 * (_r - _g) / (_b - _r) + 240
                    self._l = (self._b + self._r)
                    self._s = (self._b - self._r) / (510 - self._l) if self._l > 255 else (self._b - self._r) / self._l
                    self._h = 60 * (self._r - self._g) / (self._b - self._r) + 240
                
                else:
                    # b=>r=>g
                    # _l = (_b + _g)
                    # _s = (_l > 255) ? (_b - _g) / (510 - _l) : (_b - _g) / _l
                    # _h = 60 * (_r - _g) / (_b - _g) + 240
                    self._l = (self._b + self._g)
                    self._s = (self._b - self._g) / (510 - self._l) if self._l > 255 else (self._b - self._g) / self._l
                    self._h = 60 * (self._r - self._g) / (self._b - self._g) + 240
            
            self._l /= 510
        
        else:
            self._h = self._s = 0
            self._l = self._r / 255
