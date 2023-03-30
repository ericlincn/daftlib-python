import math

class ColorMatrix(list):

    DELTA_INDEX:list = [
        0,    0.01, 0.02, 0.04, 0.05, 0.06, 0.07, 0.08, 0.1,  0.11,
        0.12, 0.14, 0.15, 0.16, 0.17, 0.18, 0.20, 0.21, 0.22, 0.24,
        0.25, 0.27, 0.28, 0.30, 0.32, 0.34, 0.36, 0.38, 0.40, 0.42,
        0.44, 0.46, 0.48, 0.5,  0.53, 0.56, 0.59, 0.62, 0.65, 0.68, 
        0.71, 0.74, 0.77, 0.80, 0.83, 0.86, 0.89, 0.92, 0.95, 0.98,
        1.0,  1.06, 1.12, 1.18, 1.24, 1.30, 1.36, 1.42, 1.48, 1.54,
        1.60, 1.66, 1.72, 1.78, 1.84, 1.90, 1.96, 2.0,  2.12, 2.25, 
        2.37, 2.50, 2.62, 2.75, 2.87, 3.0,  3.2,  3.4,  3.6,  3.8,
        4.0,  4.3,  4.7,  4.9,  5.0,  5.5,  6.0,  6.5,  6.8,  7.0,
        7.3,  7.5,  7.8,  8.0,  8.4,  8.7,  9.0,  9.4,  9.6,  9.8, 
        10.0]
    
    IDENTITY_MATRIX:list = [
        1, 0, 0, 0, 0,
        0, 1, 0, 0, 0,
        0, 0, 1, 0, 0,
        0, 0, 0, 1, 0,
        0, 0, 0, 0, 1]
    
    LENGTH:int = len(IDENTITY_MATRIX)

    def __init__(self, matrix:list = None) -> None:

        matrix = self.__fixMatrix(matrix)
		# self.copyMatrix(((matrix.length == LENGTH) ? matrix : IDENTITY_MATRIX))
        self.__copyMatrix(matrix if len(matrix) == self.LENGTH else self.IDENTITY_MATRIX)
    
    def reset(self) -> None:
        
        for i in range(self.LENGTH):
            self[i] = self.IDENTITY_MATRIX[i]

    @property
    def brightness(self):
        raise AttributeError("brightness is write-only")
    
    # range: [-1, 1]
    @brightness.setter
    def brightness(self, value:float) -> None:
    
        value *= 100
        value = self.__limitValue(value, 100)

        # if value == 0 || isNaN(value):
        if value == 0 or math.isnan(value):
            return

        self.__multiplyMatrix([
            1, 0, 0, 0, value,
            0, 1, 0, 0, value,
            0, 0, 1, 0, value,
            0, 0, 0, 1, 0,
            0, 0, 0, 0, 1])
    
    @property
    def contrast(self):
        raise AttributeError("contrast is write-only")
    
    # range: [-1, 1]
    @contrast.setter
    def contrast(self, value:float) -> None:
    
        value *= 100
        value = self.__limitValue(value, 100)

        if value == 0 or math.isnan(value):
            return

        x:float
        if value < 0:
            x = 127 + value / 100 * 127
        else:
            x = value % 1
            if x == 0:
                x = self.DELTA_INDEX[value]
            else:
                # x = DELTA_INDEX[(p_val<<0)]; // this is how the IDE does it.
                x = self.DELTA_INDEX[(value << 0)] * (1 - x) + self.DELTA_INDEX[(value << 0) + 1] * x
                # use linear interpolation for more granularity.
            x = x * 127 + 127
        
        self.__multiplyMatrix([
            x/127, 0, 0, 0, 0.5*(127 - x),
            0, x/127, 0, 0, 0.5*(127 - x),
            0, 0, x/127, 0, 0.5*(127 - x),
            0, 0, 0, 1, 0,
            0, 0, 0, 0, 1])
    
    @property
    def saturation(self):
        raise AttributeError("saturation is write-only")
    
    # range: [-1, 1]
    @saturation.setter
    def saturation(self, value:float) -> None:
    
        value *= 100
        value = self.__limitValue(value, 100)

        if value == 0 or math.isnan(value):
            return

        # x:float = 1 + ((value > 0) ? 3 * value / 100 : value / 100);
        x:float = 1 + (3 * value / 100 if value > 0 else value / 100)
        lumR:float = 0.3086
        lumG:float = 0.6094
        lumB:float = 0.0820

        self.__multiplyMatrix([
            lumR*(1 - x)+x, lumG*(1 - x), lumB*(1 - x), 0, 0,
            lumR*(1 - x), lumG*(1 - x)+x, lumB*(1 - x), 0, 0,
            lumR*(1 - x), lumG*(1 - x), lumB*(1 - x)+x, 0, 0,
            0, 0, 0, 1, 0,
            0, 0, 0, 0, 1])
    
    @property
    def hue(self):
        raise AttributeError("hue is write-only")
    
    # range: [0, 360]
    @hue.setter
    def hue(self, value:float) -> None:
    
        value -= 180
        value = self.__limitValue(value, 180) / 180 * math.pi

        if value == 0 or math.isnan(value):
            return

        cosVal:float = math.cos(value)
        sinVal:float = math.sin(value)
        lumR:float = 0.213
        lumG:float = 0.715
        lumB:float = 0.072

        self.__multiplyMatrix([
            lumR+cosVal*(1 - lumR)+sinVal*(-lumR), lumG+cosVal*(-lumG)+sinVal*(-lumG), lumB+cosVal*(-lumB)+sinVal*(1 - lumB), 0, 0,
            lumR+cosVal*(-lumR)+sinVal*(0.143), lumG+cosVal*(1 - lumG)+sinVal*(0.140), lumB+cosVal*(-lumB)+sinVal*(-0.283), 0, 0,
            lumR+cosVal*(-lumR)+sinVal*(-(1 - lumR)), lumG+cosVal*(-lumG)+sinVal*(lumG), lumB+cosVal*(1 - lumB)+sinVal*(lumB), 0, 0,
            0, 0, 0, 1, 0,
            0, 0, 0, 0, 1])
    
    # def clone(self) -> ColorMatrix:
    def clone(self):
    
        return ColorMatrix(self)
    
    def toString(self) -> str:
    
        # return "[object ColorMatrix] [" + self.join(", ") + "]"
        return "[object ColorMatrix] [" + ", ".join(self) + "]"
    
    # multiplies one matrix against another:
    def __multiplyMatrix(self, matrix:list) -> None:
    
        col:list = []

        # for(var i:uint = 0; i < 5; i++)
        for i in range(5):
            # for(var j:uint = 0; j < 5; j++)
            for j in range(5):
                col[j] = self[j + i * 5]
            # for(j = 0; j < 5; j++)
            for j in range(5):
                val:float = 0
                # for(var k:Number = 0; k < 5; k++)
                for k in range(5):
                    val += matrix[j + k * 5] * col[k]
                
                self[j + i * 5] = val

    # make sure values are within the specified range, hue has a limit of 180, others are 100:
    def __limitValue(self, value:float, limit:float) -> float:

        # return Math.min(limit, Math.max(-limit, value));
        return min(limit, max(-limit, value))
    
    # copy the specified matrix's values to this matrix:
    def __copyMatrix(self, matrix:list) -> None:
    
        for i in range(self.LENGTH):
            self[i] = matrix[i]
    
    # makes sure matrixes are 5x5 (25 long):
    def __fixMatrix(self, matrix:list = None) -> list:
    
        if matrix == None:
            return self.IDENTITY_MATRIX

        # if matrix is ColorMatrix:
        if isinstance(matrix, ColorMatrix):
            # matrix = matrix.slice(0)
            matrix = matrix[:]

        if len(matrix) < self.LENGTH:
            # matrix = matrix.slice(0, matrix.length).concat(IDENTITY_MATRIX.slice(matrix.length, LENGTH));
            matrix = matrix[:] + self.IDENTITY_MATRIX[len(matrix):self.LENGTH]
        
        elif len(matrix) > self.LENGTH:
            # matrix = matrix.slice(0, LENGTH)
            matrix = matrix[0:self.LENGTH]
        
        return matrix