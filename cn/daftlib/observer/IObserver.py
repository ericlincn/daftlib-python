from cn.daftlib.observer.INotification import INotification

class IObserver:

    def notificationHandler(self, notification:INotification) -> None:
        pass