from cn.daftlib.errors.Error import Error
from cn.daftlib.events.ErrorEvent import ErrorEvent
from cn.daftlib.events.Event import Event
from cn.daftlib.events.EventDispatcher import EventDispatcher
from cn.daftlib.events.ProgressEvent import ProgressEvent
from cn.daftlib.net.Loader import Loader

# Usage:
# def onComplete(e):
#     print("finished")
#     ql:QueueLoader = e.target
#     print(ql.get('https://www.baidu.com/img/flexible/logo/pc/result.png'))
# def onProgress(e):
#     print(e.percent, e.bytesLoaded, e.bytesTotal)
# ql = QueueLoader()
# ql.add('https://www.baidu.com/img/flexible/logo/pc/result.png')
# ql.add('https://www.bing.com/search?q=loadable&qs=n&form=QBRE&sp=-1&lq=0&pq=loadable&sc=10-8&sk=&cvid=D203C515419349ABBA755EBDB07ED1D9&ghsh=0&ghacc=0&ghpl="')
# ql.add('https://weddingdressesguide.com/wp-content/uploads/2020/01/beach-wedding-guest-dresses-tea-length-pink-satin-summer-sexy-petalandpup-512x1024.jpg')
# ql.addEventListener(Event.COMPLETE, onComplete)
# ql.addEventListener(ProgressEvent.PROGRESS, onProgress)
# ql.start()

class QueueLoader(EventDispatcher):

    __items:list[tuple[Loader, str]] = None
    __loaded:dict = None
    __currentLoader:Loader = None
    __itemsLoaded:int = None

    def __init__(self) -> None:
        super().__init__()
        self.clear()

    def __str__(self) -> str:
        return f"[{str(self.__class__)[8:-2]}]"

    def clear(self):
        if self.hasEventListener(Event.COMPLETE):
            self.removeEventListenersForType(Event.COMPLETE)
        
        if self.__currentLoader is not None:
            self.__currentLoader.removeEventListener(Event.COMPLETE, self.__completeHandler)
            self.__currentLoader.removeEventListener(ProgressEvent.PROGRESS, self.__progressHandler)
            self.__currentLoader.removeEventListener(ErrorEvent.IO_ERROR, self.__ioErrorHandler)
            self.__currentLoader.removeEventListener(ErrorEvent.SECURITY_ERROR, self.__securityErrorHandler)
            self.__currentLoader = None
        
        self.__loaded = {}
        self.__items = []

    def add(self, url:str):
        loader = Loader()
        self.__items.append((loader, url))

    def start(self):
        if len(self.__items) <= 0:
            raise Error('Loading queue is empty')
        self.__itemsLoaded = 0
        self.__load(self.__itemsLoaded)

    def get(self, key):
        if key in self.__loaded:
            return self.__loaded[key]
        return None
    
    def __load(self, index:int):
        item = self.__items[index]
        loader:Loader = item[0]
        loader.addEventListener(Event.COMPLETE, self.__completeHandler)
        loader.addEventListener(ProgressEvent.PROGRESS, self.__progressHandler)
        loader.addEventListener(ErrorEvent.ERROR, self.__errorHandler)
        loader.addEventListener(ErrorEvent.IO_ERROR, self.__ioErrorHandler)
        loader.addEventListener(ErrorEvent.SECURITY_ERROR, self.__securityErrorHandler)

        self.__currentLoader = loader
        loader.load(item[1])

    def __completeHandler(self, e:Event):
        loader:Loader = e.target
        loader.removeEventListener(Event.COMPLETE, self.__completeHandler)
        loader.removeEventListener(ProgressEvent.PROGRESS, self.__progressHandler)
        loader.removeEventListener(ErrorEvent.ERROR, self.__errorHandler)
        loader.removeEventListener(ErrorEvent.IO_ERROR, self.__ioErrorHandler)
        loader.removeEventListener(ErrorEvent.SECURITY_ERROR, self.__securityErrorHandler)

        item = self.__items[self.__itemsLoaded]
        loader:Loader = item[0]
        self.__loaded[loader.url] = loader.content

        self.__itemsLoaded += 1
        if self.__itemsLoaded >= len(self.__items):
            self.dispatchEvent(Event(Event.COMPLETE))
            self.__currentLoader = None
        else:
            self.__load(self.__itemsLoaded)

    def __progressHandler(self, e:ProgressEvent):

        singlePercent = e.bytesLoaded / e.bytesTotal if e.bytesTotal > 0 else 1
        
        percentLoaded = singlePercent + self.__itemsLoaded
        percentTotal = len(self.__items)
        event = ProgressEvent(ProgressEvent.PROGRESS)
        event.percent = percentLoaded / percentTotal
        event.bytesLoaded = self.__itemsLoaded
        event.bytesTotal = len(self.__items)
        self.dispatchEvent(event)

    def __errorHandler(self, e:ErrorEvent):
        raise Error(e.errorMessage)
    
    def __ioErrorHandler(self, e:ErrorEvent):
        raise Error(e.errorMessage)

    def __securityErrorHandler(self, e:ErrorEvent):
        raise Error(e.errorMessage)