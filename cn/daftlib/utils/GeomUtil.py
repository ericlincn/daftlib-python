import math

from cn.daftlib.geom.Point import Point

class GeomUtil:

    PI = 3.141592653589793
    toRADIANS = PI / 180
    toDEGREES = 180 / PI

    @staticmethod
    def getScaleRatioToFill(originalWidth:float, originalHeight:float, targetWidth:float, targetHeight:float) -> float:
        widthRatio = targetWidth / originalWidth
        heightRatio = targetHeight / originalHeight
        return max(widthRatio, heightRatio)

    @staticmethod
    def getScaleRatioToFit(originalWidth:float, originalHeight:float, targetWidth:float, targetHeight:float) -> float:
        widthRatio = targetWidth / originalWidth
        heightRatio = targetHeight / originalHeight
        return min(widthRatio, heightRatio)

    @staticmethod
    def degreesToRadians(degrees:float) -> float:
        return degrees * GeomUtil.toRADIANS

    @staticmethod
    def radiansToDegrees(radians:float) -> float:
        return radians * GeomUtil.toDEGREES

    # 得到(椭)圆上点的坐标
    @staticmethod
    def getPositionOnCircle(centerX:float, centerY:float, angleInDegrees:float, radiusX:float, radiusY:float) -> Point:
        radians = GeomUtil.degreesToRadians(angleInDegrees)
        return Point(centerX + math.cos(radians) * radiusX, centerY + math.sin(radians) * radiusY)

    # 求圆心(0, 0)正圆点上的坐标
    @staticmethod
    def getResolutionByVector(angleInDegrees:float, length:float) -> Point:
        return GeomUtil.getPositionOnCircle(0, 0, angleInDegrees, length, length)

    # 取得两点中点
    @staticmethod
    def getMiddlePoint(point1:Point, point2:Point) -> Point:
        return Point.interpolate(point1, point2, .5)

    # 取得线的角度
    @staticmethod
    def getAngle(point1:Point, point2:Point) -> float:
        offsetX = point2.x - point1.x
        offsetY = point1.y - point2.y
        angle = math.atan2(offsetY, offsetX) * (180 / GeomUtil.PI)
        return angle

    @staticmethod
    def unwrapDegrees(degrees:float) -> float:
        while(degrees > 360):
            degrees -= 360
        while(degrees < 0):
            degrees += 360
        return degrees

    @staticmethod
    def getDegreesShortDelta(degreesFrom:float, degreesTo:float) -> float:
        degreesFrom = GeomUtil.unwrapDegrees(degreesFrom)
        degreesTo = GeomUtil.unwrapDegrees(degreesTo)
        delta = degreesTo - degreesFrom
        if(delta > 180):
            delta -= 360
        if(delta < -180):
            delta += 360
        return delta

    # 判断两线段是否相交
    @staticmethod
    def getIntersect(point1:Point, point2:Point, point3:Point, point4:Point) -> Point:
        v1 = Point()
        v2 = Point()
        d = 0
        intersectPoint = Point()

        v1.x = point2.x - point1.x
        v1.y = point2.y - point1.y
        v2.x = point4.x - point3.x
        v2.y = point4.y - point3.y

        d = v1.x * v2.y - v1.y * v2.x
        if(d == 0):
            #points are collinear
            return None

        a = point3.x - point1.x
        b = point3.y - point1.y
        t = (a * v2.y - b * v2.x) / d
        s = (b * v1.x - a * v1.y) / -d
        if(t < 0 or t > 1 or s < 0 or s > 1):
            #line segments don't intersect
            return None

        intersectPoint = Point()
        intersectPoint.x = point1.x + v1.x * t
        intersectPoint.y = point1.y + v1.y * t
        return intersectPoint

    # 获取两正圆公切线,返回值可能为null或2条外切线或2条外切线+2条内切线
    @staticmethod
    def getTangents(x1:float, y1:float, radius1:float, x2:float, y2:float, radius2:float) -> list:
        dsq = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
        if dsq <= (radius1 - radius2) * (radius1 - radius2):
            return None
        
        d = math.sqrt(dsq)
        vx = (x2 - x1) / d
        vy = (y2 - y1) / d
        
        result = []
        
        sign1 = 1
        while sign1 >= -1:
            c = (radius1 - sign1 * radius2) / d
            if c * c > 1.0:
                sign1 -= 2
                continue
            
            h = math.sqrt(max(0.0, 1.0 - c*c))
            sign2 = 1
            while sign2 >= -1:
                nx = vx * c - sign2 * h * vy
                ny = vy * c + sign2 * h * vx
                result.append((Point(x1 + radius1 * nx, y1 + radius1 * ny), Point(x2 + sign1 * radius2 * nx, y2 + sign1 * radius2 * ny)))
                sign2 -= 2
            sign1 -= 2
        
        return result