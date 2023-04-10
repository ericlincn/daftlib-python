class Error(BaseException):

    DEFAULT_TO_STRING:str = "Error"

    def __init__(self, message:str = "", id:int = 0) -> None:
        self.__message = message
        self.__errorID = id

    def __str__(self) -> str:
        return f"[{str(self.__class__)[8:-2]}](message={self.__message if self.__message else Error.DEFAULT_TO_STRING}, errorID={self.errorID})"

    @property
    def message(self) -> str:
        return self.__message
    
    @property
    def errorID(self) -> int:
        return self.__errorID