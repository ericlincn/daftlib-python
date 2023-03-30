from cn.daftlib.events.Event import Event

class IEventDispatcher:

    # def addEventListener(type:str, listener:function, useCapture:bool = False, useWeakReference:bool = False) -> None:
    def addEventListener(self, type:str, listener:callable, useCapture:bool = False, useWeakReference:bool = False) -> None:
        pass

    def dispatchEvent(self, event:Event) -> bool:
        pass

    def hasEventListener(self, type:str) -> bool:
        pass

    def removeEventListener(self, type:str) -> None:
        pass

    def willTrigger(self, type:str) -> bool:
        pass