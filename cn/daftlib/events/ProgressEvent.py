from cn.daftlib.events.Event import Event

class ProgressEvent(Event):

    PROGRESS:str = "progress"

    bytesLoaded:float
    bytesTotal:float
    percent:float

    def __init__(self, type:str) -> None:
        super().__init__(type)