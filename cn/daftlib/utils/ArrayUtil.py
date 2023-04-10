import random
import sys

class ArrayUtil:

    @staticmethod
    def shuffle(target:list) -> None:
        for i in range(len(target)):
            j = int(len(target) * random.random())
            a = target[i]
            b = target[j]
            target[i] = b
            target[j] = a

    @staticmethod
    def sortByAttribute(target:list, attribute:str) -> None:
        target.sort(key=lambda x: getattr(x, attribute))

    @staticmethod
    def switchElements(target:list, index1:int, index2:int) -> None:
        a = target[index1]
        b = target[index2]
        target[index1] = b
        target[index2] = a

    @staticmethod
    def getDistinctList(target:list) -> list:
        obj = {}
        def filter_fn(item):
            nonlocal obj
            if not obj.get(item):
                obj[item] = True
                return True
            else:
                return False
        return list(filter(filter_fn, target))

    @staticmethod
    def getShortDistance(index1, index2, length) -> int:
        min_index = min(index1, index2)
        max_index = max(index1, index2)

        if max_index >= length:
            return sys.maxsize

        dist = index2 - index1
        if abs(dist) <= (length / 2):
            return dist
        else:
            return int(-dist / abs(dist) * (min_index + length - max_index))