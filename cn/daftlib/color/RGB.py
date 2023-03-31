from cn.daftlib.color.IColor import IColor

class RGB(IColor):
    
    _r:int
    _g:int
    _b:int

    def __init__(self, r=0, g=0, b=0):
        self._r = r
        self._g = g
        self._b = b

    @property
    def value(self):
        return (self._r << 16) | (self._g << 8) | self._b

    @value.setter
    def value(self, value):
        self._r = value >> 16
        self._g = (value & 0x00ff00) >> 8
        self._b = value & 0x0000ff

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, value):
        self._r = max(0, min(255, value))

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, value):
        self._g = max(0, min(255, value))

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        self._b = max(0, min(255, value))
