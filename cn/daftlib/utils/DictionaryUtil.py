class DictionaryUtil:

    @staticmethod
    def get_any_key(target:dict):
        return next(iter(target.keys()))

    @staticmethod
    def get_any_value(target:dict):
        return next(iter(target.values()))