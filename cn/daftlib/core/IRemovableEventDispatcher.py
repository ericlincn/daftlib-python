class IRemovableEventDispatcher:

    def removeEventsForType(self, type:str) -> None:
        pass

    def removeEventsForListener(self, listener:callable) -> None:
        pass

    def removeEventListeners(self) -> None:
        pass