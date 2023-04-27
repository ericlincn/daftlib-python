import random

class ColorUtil:

    @staticmethod
    def toHex(color:int) -> str:
        return hex(color)
    
    @staticmethod
    def toRGB(argb:int) -> int:
        rgb = (argb & 0xFFFFFF)
        return rgb

    @staticmethod
    def toARGB(rgb:int, alpha:float = 1) -> int:
        argb = rgb
        argb += (alpha * 255 << 24)
        return argb

    @staticmethod
    def getRandomColor() -> int:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return r << 16 | g << 8 | b

    @staticmethod
    def getGray(gray:int) -> int:
        gray = max(0, min(255, gray))
        r = g = b = gray & 0xFF
        return r << 16 | g << 8 | b

    @staticmethod
    def isDarkColor(rgb) -> bool:
        r = rgb >> 16 & 0xFF
        g = rgb >> 8  & 0xFF
        b = rgb & 0xFF
        perceivedLuminosity = (0.299 * r + 0.587 * g + 0.114 * b)
        return perceivedLuminosity < 70

    @staticmethod
    def getAverageColor(colors) -> int:
        r = 0
        g = 0
        b = 0
        l = len(colors)
        i = 0
        while i < l:
            r += colors[i] >> 16
            g += (colors[i] & 0x00ff00) >> 8
            b += colors[i] & 0x0000ff
            i += 1
        r /= l
        g /= l
        b /= l
        return int(r) << 16 | int(g) << 8 | int(b)
    
    @staticmethod
    def getDifference(color1:int, color2:int):
        # convert to (r, g, b)
        color1_rgb = (color1 >> 16, (color1 & 0x00ff00) >> 8, color1 & 0x0000ff)
        color2_rgb = (color2 >> 16, (color2 & 0x00ff00) >> 8, color2 & 0x0000ff)
        averageR = (color1_rgb[0] + color2_rgb[0]) * 0.5
        diff = ((2 + averageR / 255) * pow(color1_rgb[0] - color2_rgb[0], 2) + 4 * pow(color1_rgb[1] - color2_rgb[1], 2) + (2 + (255 - averageR) / 255) * pow(color1_rgb[2]- color2_rgb[2], 2)) / (3 * 255) / (3 * 255)
        return diff