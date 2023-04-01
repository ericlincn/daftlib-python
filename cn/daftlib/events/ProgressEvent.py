from cn.daftlib.events.Event import Event

class ProgressEvent(Event):

    PROGRESS:str = "progress"
    SOCKET_DATA:str = "socketData"

    bytesLoaded:float
    bytesTotal:float
    percent:float

    def __init__(self, type: str, bubbles: bool = False, cancelable: bool = False) -> None:
        super().__init__(type, bubbles, cancelable)