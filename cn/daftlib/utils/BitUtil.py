class BitUtil:

    # 获取value二进制下第n位（从右往左数，从1开始）的值（0或1）
    @staticmethod
    def getBitN(value, n):
        return (value >> (n - 1)) & 1

    # 将value二进制下第n位设置为1，并返回设置后的值
    @staticmethod
    def setBitN1(value, n):
        return value | (1 << (n - 1))

    # 将value二进制下第n位设置为0，并返回设置后的值
    @staticmethod
    def setBitN0(value, n):
        return value & ~(1 << (n - 1))

    # 判断a和b的符号是否相反
    @staticmethod
    def oppositeSigns(a, b):
        return (a ^ b) < 0

    # 判断value是否为奇数
    @staticmethod
    def isOdd(value):
        return (value & 1) == 1

    # 计算value的绝对值
    @staticmethod
    def abs(value):
        return (value ^ (value >> 31)) - (value >> 31)

    # 返回a和b中的最大值
    @staticmethod
    def max(a, b):
        return a ^ ((a ^ b) & -(1 if a < b else 0))

    # 返回a和b中的最小值
    @staticmethod
    def min(a, b):
        return b ^ ((a ^ b) & -(1 if a < b else 0))

    # 返回a和b的平均值，其中a和b必须为整数
    @staticmethod
    def average(a, b):
        return (a & b) + ((a ^ b) >> 1)

    # 判断value是否为2的幂次方
    @staticmethod
    def isPower2(value):
        return ((value & (value - 1)) == 0) and (value != 0)

    # 将value乘以2
    @staticmethod
    def mul2(value):
        return value << 1

    # 将value除以2
    @staticmethod
    def div2(value):
        return value >> 1

    # 返回value除以2的余数（0或1）
    @staticmethod
    def mod2(value):
        return value & 1

    # 对value进行2的power次幂取模运算
    @staticmethod
    def mod2exp(value, power):
        return value & (2 ^ power - 1)

    # 将value乘以2的power次幂
    @staticmethod
    def mul2exp(value, power):
        return value << power

    # 将value除以2的power次幂
    @staticmethod
    def div2exp(value, power):
        return value >> power