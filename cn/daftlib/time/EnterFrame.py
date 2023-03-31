from cn.daftlib.events.Event import Event
from cn.daftlib.events.EventDispatcher import EventDispatcher
import threading
import time

class EnterFrame(EventDispatcher):

    __fps:int
    
    def __init__(self, fps:int = 60, target = None) -> None:
        super().__init__(target)
        self.__fps = fps
        thread = threading.Thread(target=self.__timer)
        thread.start()

    def __timer(self):
        start_time = time.time()
        while True:
            time.sleep(max(1/self.__fps - (time.time() - start_time), 0))
            start_time = time.time()
            self.dispatchEvent(Event(Event.ENTER_FRAME))