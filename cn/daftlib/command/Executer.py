from cn.daftlib.interfaces.IDestroyable import IDestroyable
from cn.daftlib.events.Event import Event
from cn.daftlib.command.ICommand import ICommand
from cn.daftlib.events.EventDispatcher import EventDispatcher

import timeit

class Executer(EventDispatcher, IDestroyable):

    __commandsArr:list
    __undoCommand:ICommand

    def __init__(self) -> None:

        super().__init__()
        self.reset()

    def __str__(self) -> str:
        return f"[{str(self.__class__)[8:-2]}]"
    
    def reset(self) -> None:

        self.__commandsArr = []
        self.__undoCommand = None

    def run(self) -> None:

        # start = timeit.default_timer()

        l = len(self.__commandsArr)
        
        if l > 0:
            current:ICommand = self.__commandsArr[0]

            try:
                self.__undoCommand = self.__commandsArr.pop(0)
            except IndexError as e:
                print("IndexError: ", e, "@class Executer")
            
            current.addEventListener(Event.COMPLETE, self.__completeHandler)
            current.execute()
            
        else:
            self.dispatchEvent(Event(Event.COMPLETE))

        # print(timeit.default_timer() - start)

    def __completeHandler(self, e:Event) -> None:
        
        current:ICommand = e.target
        current.removeEventListener(Event.COMPLETE, self.__completeHandler)

        self.run()

    def destroy(self) -> None:

        self.reset()
        self.removeAllEventListeners()

    def addCommmand(self, command:ICommand):

        self.__commandsArr.append(command)
    
    def addPriorityCommmand(self, command:ICommand):

        self.__commandsArr.insert(0, command)
