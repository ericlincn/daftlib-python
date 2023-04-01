from cn.daftlib.events.Event import Event

class ErrorEvent(Event):

    ERROR:str = "error"
    IO_ERROR:str  = "ioError"
    SECURITY_ERROR:str = "securityError"

    errorMessage:str
    errorID:int

    def __init__(self, type: str, bubbles: bool = False, cancelable: bool = False) -> None:
        super().__init__(type, bubbles, cancelable)