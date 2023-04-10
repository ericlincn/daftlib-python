from cn.daftlib.observer.INotification import INotification

class Notification(INotification):

    __name:str
    __body:object

    def __init__(self, name:str, body:object) -> None:
        
        self.__name = name
        self.__body = body

    def __str__(self) -> str:
        return f"[{str(self.__class__)[8:-2]}](name={self.name})"

    @property
    def name(self) -> str:
        
        return self.__name

    @property
    def body(self) -> object:
        
        return self.__body