from cn.daftlib.observer.INotification import INotification

class IObserver:

    def handlerNotification(self, notification:INotification) -> None:
        pass