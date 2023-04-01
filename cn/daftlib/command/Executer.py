from cn.daftlib.events.Event import Event
from cn.daftlib.command.ICommand import ICommand
from cn.daftlib.core.RemovableEventDispatcher import RemovableEventDispatcher
import timeit

class Executer(RemovableEventDispatcher):

    __commandsArr:list
    __undoCommand:ICommand

    def __init__(self, target = None) -> None:

        super().__init__(target)
        self.reset()
    
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
        
        current = e.target
        current.removeEventListener(Event.COMPLETE, self.__completeHandler)

        self.run()

    def destroy(self) -> None:

        self.reset()
        super().destroy()

    def addCommmand(self, command:ICommand):

        self.__commandsArr.append(command)
    
    def addPriorityCommmand(self, command:ICommand):

        self.__commandsArr.insert(0, command)

    # def printCommmands(self):

    #     s = ""
    #     l = len(self.__commandsArr)
    #     if l > 0:
    #         for i in range(0, l):
    #             c = str(type(self.__commandsArr[i]))
    #             c = c.replace("<class '", "")
    #             c = c.replace("'>", "")
    #             c = c.split(".")[-1]

    #             if c == "ICommand": c = "."
    #             else: c = c.replace("Command", ""); c += " "
                
    #             s += c
    #     return s