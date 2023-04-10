import random

class NumberUtil:
    @staticmethod
    def abs(x:float) -> float:
        return -x if x < 0 else x

    @staticmethod
    def min(x:float, y:float) -> float:
        return x if x < y else y

    @staticmethod
    def max(x:float, y:float) -> float:
        return x if x > y else y

    @staticmethod
    def floor(n:float) -> int:
        ni = int(n)
        return ni - 1 if n < 0 and n != ni else ni

    @staticmethod
    def round(n:float) -> int:
        return int(n - 0.5 if n < 0 else n + 0.5)

    @staticmethod
    def ceil(n:float) -> int:
        ni = int(n)
        return ni + 1 if n >= 0 and n != ni else ni

    @staticmethod
    def getDecimal(value:float) -> float:
        if value < 1:
            return value
        arr = str(value).split(".")
        if arr[1]:
            return float("0." + arr[1])
        return 0

    @staticmethod
    def clamp(value:float, min:float, max:float) -> float:
        return NumberUtil.min(max, NumberUtil.max(value, min))

    @staticmethod
    def getPercent(value:float, min:float, max:float) -> float:
        return (value - min) / (max - min)

    @staticmethod
    def roundDecimalToPlace(value:float, place:int) -> float:
        p = 10 ** place
        return NumberUtil.round(value * p) / p

    @staticmethod
    def randomInRange(min:float, max:float) -> float:
        return min + (random.random() * (max - min))

    @staticmethod
    def randomBoolean() -> bool:
        return random.random() < 0.5

    @staticmethod
    def randomWave() -> int:
        return NumberUtil.floor(random.random() * 2) * 2 - 1

    @staticmethod
    def extractPlusMinus(value:float) -> int:
        return int(value / NumberUtil.abs(value))