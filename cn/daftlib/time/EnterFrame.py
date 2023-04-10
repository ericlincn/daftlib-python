from cn.daftlib.events.Event import Event
from cn.daftlib.events.EventDispatcher import EventDispatcher
import threading
import time

class EnterFrame(EventDispatcher):

    __fps:int
    __isRunning:bool
    
    def __init__(self, fps:int = 60, target = None) -> None:
        super().__init__(target)
        self.__fps = fps
        self.__isRunning = True
        thread = threading.Thread(target=self.__timer)
        thread.start()

    def __timer(self) -> None:
        start_time = time.time()
        while self.__isRunning:
            time.sleep(max(1/self.__fps - (time.time() - start_time), 0))
            start_time = time.time()
            self.dispatchEvent(Event(Event.ENTER_FRAME))

    def __str__(self) -> str:
        return f"[{str(self.__class__)[8:-2]}](fps={self.__fps})"

    def pause(self) -> None:
        self.__isRunning = False

    def resume(self) -> None:
        self.__isRunning = True