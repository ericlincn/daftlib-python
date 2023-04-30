from typing import Callable

class Listener:

    callback:Callable
    priority:int

    def __init__(self, callback:Callable, priority:int) -> None:
        self.callback = callback
        self.priority = priority
    def match(self, callback:Callable) -> bool:
        return self.callback == callback

# Usage:
# def onComplete():
#     print("complete")
# def onComplete2():
#     print("complete2")
# def onActive(data):
#     print("active", data)
# class B:
#     active:Signal = Signal()
#     complete:Signal = Signal()
# b = B()
# b.complete.connect(onComplete)
# b.complete.connect(onComplete2)
# b.active.connect(onActive)
# b.complete.emit()
# b.active.emit([1,2,3])
# b.complete.disconnectAll()
# b.complete.emit()

class Signal:

    __slots:list[Listener]

    def __init__(self):
        self.__slots = []

    def connect(self, listener:Callable, priority:int = 0) -> None:
        if listener == None: return

        for i in range(0, len(self.__slots)):
                if self.__slots[i].match(listener): return
        
        self.__addListenerByPriority(self.__slots, Listener(listener, priority))
    
    def __addListenerByPriority(self, list:list, listener:Listener) -> None:
        numElements = len(list)
        addAtPosition = numElements

        for i in range(0, numElements):
            if list[i].priority < listener.priority:

                addAtPosition = i
                break

        list.insert(addAtPosition, listener)
    
    def disconnect(self, listener:Callable) -> None:
        for i in range(0, len(self.__slots)):
            if self.__slots[i].match(listener):
                self.__slots.pop(i)
                break

    def emit(self, *args, **kwargs) -> None:
        for listener in self.__slots:
            listener.callback(*args, **kwargs)

    def disconnectAll(self) -> None:
        self.__slots = []