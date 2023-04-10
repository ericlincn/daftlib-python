from cn.daftlib.events.IEventDispatcher import IEventDispatcher

class ICommand(IEventDispatcher):

    def execute(self):
        pass

    def undo(self):
        pass