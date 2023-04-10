from cn.daftlib.color.RGB import RGB

class ARGB(RGB):

    _a:int

    def __init__(self, r:int = 0, g:int = 0, b:int = 0, a:int = 255) -> None:
        super().__init__(r, g, b)
        self._a = a

    def __str__(self) -> str:
        return f"[{str(self.__class__)[8:-2]}](r={self.r}, g={self.g}, b={self.b}, alpha={self.alpha})"

    @property
    def value(self) -> int:
        return (self._a << 24) | (self.r << 16) | (self.g << 8) | self.b

    @value.setter
    def value(self, value32:int) -> None:
        self._a = value32 >> 24
        self._a = 256 + self._a if self._a < 0 else self._a
        self.r = (value32 >> 16) & 0xff
        self.g = (value32 >> 8) & 0xff
        self.b = value32 & 0xff

    @property
    def alpha(self) -> int:
        return self._a

    @alpha.setter
    def alpha(self, value:int) -> None:
        self._a = max(0, min(255, value))