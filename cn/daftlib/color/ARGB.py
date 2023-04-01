from cn.daftlib.color.RGB import RGB

class ARGB(RGB):

    _a:int

    def __init__(self, r=0, g=0, b=0, a=255):
        super().__init__(r, g, b)
        self._a = a

    @property
    def value(self):
        return (self._a << 24) | (self.r << 16) | (self.g << 8) | self.b

    @value.setter
    def value(self, value32):
        self._a = value32 >> 24
        self._a = 256 + self._a if self._a < 0 else self._a
        self.r = (value32 >> 16) & 0xff
        self.g = (value32 >> 8) & 0xff
        self.b = value32 & 0xff

    @property
    def alpha(self):
        return self._a

    @alpha.setter
    def alpha(self, value):
        self._a = max(0, min(255, value))