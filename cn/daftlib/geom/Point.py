import math

class Point:

    x:float
    y:float

    def __init__(self, x:float = 0, y:float = 0) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"[{str(self.__class__)[8:-2]}](x={self.x}, y={self.y})"

    def add(self, point):
        return Point(point.x + self.x, point.y + self.y)
    
    def clone(self):
        return Point(self.x, self.y)
    
    def copyFrom(self, source) -> None:
        self.x = source.x
        self.y = source.y

    @staticmethod
    def distance(point1, point2) -> float:
        dx = point1.x - point2.x
        dy = point1.y - point2.y
        return math.sqrt(dx * dx + dy * dy)
    
    def equals(self, toCompare) -> bool:
        return toCompare != None and toCompare.x == self.x and toCompare.y == self.y
    
    @staticmethod
    def interpolate(point1, point2, f:float):
        return Point(point2.x + f * (point1.x - point2.x), point2.y + f * (point1.y - point2.y))
    
    def normalize(self, thickness:float) -> None:
        if self.x == 0 and self.y == 0:
            return
        else:
            norm = thickness / math.sqrt(self.x * self.x + self.y * self.y)
            self.x *= norm
            self.y *= norm

    def offset(self, dx:float, dy:float) -> None:
        self.x += dx
        self.y += dy

    def polar(self, len:float, angle:float):
        return Point(len * math.cos(angle), len * math.sin(angle))
    
    def subtract(self, point):
        return Point(self.x - point.x, self.y - point.y)
    
    @property
    def length(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)