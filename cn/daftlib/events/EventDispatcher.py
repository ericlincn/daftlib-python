from typing import Callable
from cn.daftlib.events.Event import Event
from cn.daftlib.events.IEventDispatcher import IEventDispatcher

class Listener:

    callback:Callable
    priority:int

    # callback:function
    def __init__(self, callback:Callable, priority:int) -> None:
        self.callback = callback
        self.priority = priority
    # callback:function
    def match(self, callback:Callable) -> bool:
        return self.callback == callback

class DispatchIterator:

    active:bool
    index:int
    __isCopy:bool
    __list:list

    def __init__(self, list:list) -> None:
        self.active = False
        self.reset(list)
    def __iter__(self):
        return self
    def reset(self, list:list) -> None:
        self.__list = list
        self.__isCopy = False
        self.index = 0
    def copy(self) -> None:
        if self.__isCopy == False:
            self.__list = self.__list.copy()
            self.__isCopy = True
    def hasNext(self) -> bool:
        return self.index < len(self.__list)
    # def next(self) -> Listener:
    #     self.index += 1
    #     return self.__list[self.index]
    def __next__(self) -> Listener:
        if self.hasNext():
            out = self.__list[self.index]
            self.index += 1
            # print(self.index, len(self.__list))
            return out
        else:
            raise StopIteration()
    def remove(self, listener:Listener, listIndex:int) -> None:
        if self.active:
            if self.__isCopy == False:
                if listIndex < self.index:
                    self.index -= 1
            else:
                for i in range(self.index, len(self.__list)):
                    if self.__list[i] == listener:
                        self.__list.pop(i)
                        break
    def start(self) -> None:
        self.active = True
    def stop(self) -> None:
        self.active = False

# Usage:
# def onComplete(e):
#     print("complete", e.type)
# def onComplete2(e):
#     print("complete2", e.type)
# def onActive(e):
#     print("active", e.type)
# dispatcher = EventDispatcher()
# dispatcher.addEventListener(Event.COMPLETE, onComplete)
# dispatcher.addEventListener(Event.ACTIVATE, onActive)
# dispatcher.addEventListener(Event.COMPLETE, onComplete2)
# dispatcher.addEventListener(Event.ACTIVATE, onComplete2)
# dispatcher.dispatchEvent(Event(Event.COMPLETE))
# dispatcher.dispatchEvent(Event(Event.ACTIVATE))
# dispatcher.dispatchEvent(Event(Event.COMPLETE))
# print("removing...")
# dispatcher.removeEventListenersForListener(onComplete2)
# dispatcher.dispatchEvent(Event(Event.COMPLETE))
# dispatcher.dispatchEvent(Event(Event.ACTIVATE))
# dispatcher.dispatchEvent(Event(Event.COMPLETE))

class EventDispatcher(IEventDispatcher):

    __eventMap:dict
    __iterators:dict

    def __init__(self) -> None:
        
        self.__eventMap = None
        # self.__iterators = None

    def __str__(self) -> str:
        return f"[{str(self.__class__)[8:-2]}]"

    # callback:function
    def addEventListener(self, type:str, listener:Callable, priority:int = 0) -> None:
        
        if listener == None: return

        if self.__eventMap == None:
            self.__eventMap = dict()
            self.__iterators = dict()

        # if self.__eventMap[type] == None:
        if type not in self.__eventMap:
            list = []
            list.append(Listener(listener, priority))

            iterator = DispatchIterator(list)

            self.__eventMap[type] = list
            self.__iterators[type] = [iterator]
        else:
            list = self.__eventMap[type]

            for i in range(0, len(list)):
                if list[i].match(listener): return

            iterators = self.__iterators[type]
            
            for iterator in iterators:
                if iterator.active:
                    iterator.copy()

            self.__addListenerByPriority(list, Listener(listener, priority))
    
    def dispatchEvent(self, event:Event) -> bool:

        event.target = self
        return self.__dispatchEvent(event)

    def hasEventListener(self, type:str) -> bool:

        if self.__eventMap == None: return False

        # if self.__eventMap[type]: return True
        # else: return False
        return type in self.__eventMap

    # callback:function
    def removeEventListener(self, type:str, listener:Callable) -> None:

        if self.__eventMap == None or listener == None: return

        # Could cause KeyError
        # list = self.__eventMap[type]
        list = self.__eventMap.get(type)
        if list == None: return

        iterators = self.__iterators[type]

        for i in range(0, len(list)):
            if list[i].match(listener):
                for iterator in iterators:
                    iterator.remove(list[i], i)
                # list.splice(i, 1);
                list.pop(i)
                break

        if len(list) == 0:
            del self.__eventMap[type]
            del self.__iterators[type]
        
        # if (!__eventMap.iterator().hasNext())
        if len(self.__eventMap) <= 0:
            self.__eventMap = None
            self.__iterators = None

    def willTrigger(self, type:str) -> bool:

        return self.hasEventListener(type)

    def __dispatchEvent(self, event:Event) -> bool:

        if self.__eventMap == None or event == None: return True

        type = event.type

        if type not in self.__eventMap: return True

        list = self.__eventMap[type]

        iterators = self.__iterators[type]
        iterator = iterators[0]

        if iterator.active:
            iterator = DispatchIterator(list)
            iterators.append(iterator)

        iterator.start()

        for listener in iterator:
            if listener == None: continue

            listener.callback(event)

        iterator.stop()

        if iterator != iterators[0]:
            iterators.remove(iterator)
        else:
            iterator.reset(list)

        return True

    def __addListenerByPriority(self, list:list, listener:Listener) -> None:

        numElements = len(list)
        addAtPosition = numElements

        for i in range(0, numElements):
            if list[i].priority < listener.priority:

                addAtPosition = i
                break

        list.insert(addAtPosition, listener)

    def removeAllEventListeners(self) -> None:

        self.__eventMap = None
        self.__iterators = None
    
    def removeEventListenersForType(self, type: str) -> None:

        if self.__eventMap == None : return

        list = self.__eventMap.get(type)
        if list == None: return

        del self.__eventMap[type]
        del self.__iterators[type]

        if len(self.__eventMap) <= 0:
            self.__eventMap = None
            self.__iterators = None

    def removeEventListenersForListener(self, listener:Callable) -> None:
        
        if self.__eventMap == None or listener == None: return

        for type in self.__eventMap:
            list = self.__eventMap.get(type)
            if list == None: continue

            iterators = self.__iterators[type]

            for i in range(0, len(list)):
                if list[i].match(listener):
                    for iterator in iterators:
                        iterator.remove(list[i], i)
                    # list.splice(i, 1);
                    list.pop(i)
                    break

            if len(list) == 0:
                del self.__eventMap[type]
                del self.__iterators[type]
        
        # if (!__eventMap.iterator().hasNext())
        if len(self.__eventMap) <= 0:
            self.__eventMap = None
            self.__iterators = None