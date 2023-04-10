import timeit

class Stopwatch:

    __start = 0

    @staticmethod
    def start():
        Stopwatch.__start = timeit.default_timer()

    @staticmethod
    def time():
        return timeit.default_timer() - Stopwatch.__start