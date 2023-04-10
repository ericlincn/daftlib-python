from cn.daftlib.geom.Point import Point

class Rectangle:

    x:float
    y:float
    width:float
    height:float

    def __init__(self, x:float = 0, y:float = 0, width:float = 0, height:float = 0) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self) -> str:
        return f"[{str(self.__class__)[8:-2]}](x={self.x}, y={self.y}, width={self.width}, height={self.height})"

    def clone(self):
        return Rectangle(self.x, self.y, self.width, self.height)
    
    def contains(self, x:float, y:float) -> bool:
        return x >= self.x and y >= self.y and x < self.right and y < self.bottom
    
    def containsPoint(self, point:Point) -> bool:
        return self.contains(point.x, point.y)
    
    def containsRect(self, rect) -> bool:
        if rect.width <= 0 or rect.height <= 0:
            return rect.x > self.x and rect.y > self.y and rect.right < self.right and rect.bottom < self.bottom
        else:
            return rect.x >= self.x and rect.y >= self.y and rect.right <= self.right and rect.bottom <= self.bottom
        
    def copyFrom(self, source) -> None:
        self.x = source.x
        self.y = source.y
        self.width = source.width
        self.height = source.height

    def equals(self, toCompare) -> bool:
        if toCompare == self: return True
        else:
            return toCompare != None and self.x == toCompare.x and self.y == toCompare.y and self.width == toCompare.width and self.height == toCompare.height
        
    def inflate(self, dx:float, dy:float) -> None:
        self.x -= dx
        self.width += dx * 2
        self.y -= dy
        self.height += dy * 2

    def inflatePoint(self, point:Point) -> None:
        self.inflate(point.x, point.y)

    def intersection(self, toIntersect):
        x0 = max(self.x, toIntersect.x)
        x1 = min(self.right, toIntersect.right)

        if x1 <= x0:
            return Rectangle()

        y0 = max(self.y, toIntersect.y)
        y1 = min(self.bottom, toIntersect.bottom)

        if y1 <= y0:
            return Rectangle()

        return Rectangle(x0, y0, x1 - x0, y1 - y0)

    def intersects(self, toIntersect) -> bool:
        x0 = max(self.x, toIntersect.x)
        x1 = min(self.right, toIntersect.right)

        if x1 <= x0:
            return False

        y0 = max(self.y, toIntersect.y)
        y1 = min(self.bottom, toIntersect.bottom)

        return y1 > y0
    
    def isEmpty(self) -> bool:
        return (self.width <= 0 or self.height <= 0)

    def offset(self, dx:float, dy:float) -> None:
        self.x += dx
        self.y += dy

    def offsetPoint(self, point:Point) -> None:
        self.x += point.x
        self.y += point.y

    def setEmpty(self) -> None:
        self.x = self.y = self.width = self.height = 0

    def union(self, toUnion):
        if self.width == 0 or self.height == 0:
            return toUnion.clone()
        elif toUnion.width == 0 or toUnion.height == 0:
            return self.clone()

        x0 = self.x if self.x > toUnion.x else toUnion.x
        x1 = toUnion.right if self.right < toUnion.right else self.right
        y0 = self.y if self.y > toUnion.y else toUnion.y
        y1 = toUnion.bottom if self.bottom < toUnion.bottom else self.bottom

        return Rectangle(x0, y0, x1 - x0, y1 - y0)

    @property
    def bottom(self) -> float:
        return self.y + self.height

    @bottom.setter
    def bottom(self, b:float) -> float:
        self.height = b - self.y
        return b

    @property
    def left(self) -> float:
        return self.x

    @left.setter
    def left(self, l:float) -> float:
        self.width -= l - self.x
        self.x = l
        return l

    @property
    def right(self) -> float:
        return self.x + self.width

    @right.setter
    def right(self, r:float) -> float:
        self.width = r - self.x
        return r

    @property
    def size(self) -> Point:
        return Point(self.width, self.height)

    @size.setter
    def size(self, p:Point) -> Point:
        self.width = p.x
        self.height = p.y
        return p.clone()

    @property
    def top(self) -> float:
        return self.y

    @top.setter
    def top(self, t:float) -> float:
        self.height -= t - self.y
        self.y = t
        return t
