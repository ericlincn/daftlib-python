from cn.daftlib.color.IColor import IColor

class RGB(IColor):
    
    _r:int
    _g:int
    _b:int

    def __init__(self, r:int = 0, g:int = 0, b:int = 0) -> None:
        self._r = r
        self._g = g
        self._b = b

    def __str__(self) -> str:
        return f"[{str(self.__class__)[8:-2]}](r={self.r}, g={self.g}, b={self.b})"

    @property
    def value(self) -> int:
        return (self._r << 16) | (self._g << 8) | self._b

    @value.setter
    def value(self, value:int) -> None:
        self._r = value >> 16
        self._g = (value & 0x00ff00) >> 8
        self._b = value & 0x0000ff

    @property
    def r(self) -> int:
        return self._r

    @r.setter
    def r(self, value:int) -> None:
        self._r = max(0, min(255, value))

    @property
    def g(self) -> int:
        return self._g

    @g.setter
    def g(self, value:int) -> None:
        self._g = max(0, min(255, value))

    @property
    def b(self) -> int:
        return self._b

    @b.setter
    def b(self, value:int) -> None:
        self._b = max(0, min(255, value))
