from cn.daftlib.events.ErrorEvent import ErrorEvent
from cn.daftlib.events.Event import Event
from cn.daftlib.events.ProgressEvent import ProgressEvent
from cn.daftlib.net.ILoadable import ILoadable
from cn.daftlib.events.EventDispatcher import EventDispatcher
import requests

# Usage:
# def onComplete(e):
#     l = e.target
#     print("onComplete", l.content, l.url)
# def onProgress(e):
#     print("onProgress", e.percent, str(e.bytesLoaded) + "/" + str(e.bytesTotal))
# l = Loader()
# l.addEventListener(Event.COMPLETE, onComplete)
# l.addEventListener(ProgressEvent.PROGRESS, onProgress)
# l.load("https://www.baidu.com/img/flexible/logo/pc/result.png")
# # l.load("https://www.bing.com/search?q=loadable&qs=n&form=QBRE&sp=-1&lq=0&pq=loadable&sc=10-8&sk=&cvid=D203C515419349ABBA755EBDB07ED1D9&ghsh=0&ghacc=0&ghpl=")

class Loader(EventDispatcher, ILoadable):

    __content:bytes = None
    __url:str = None

    def __init__(self, target = None) -> None:
        super().__init__(target)

    @property
    def content(self) -> bytes:
        return self.__content
    
    @property
    def url(self) -> str:
        return self.__url
    
    def load(self, url:str) -> None:

        self.__url = url

        try:
            with requests.get(url, stream = True) as response:
                
                if response.status_code == 200:
                    content_length = int(response.headers.get('content-length', 0))
                    content = b''
                    for chunk in response.iter_content(chunk_size = 1024):
                        content += chunk
                        event = ProgressEvent(ProgressEvent.PROGRESS)
                        event.bytesLoaded = len(content)
                        event.bytesTotal = content_length

                        if content_length > 0:
                            event.percent = len(content) / content_length
                        else:
                            event.percent = -1
                        
                        self.dispatchEvent(event)
                    self.__content = content

                else:
                    error = ErrorEvent(ErrorEvent.ERROR)
                    error.errorMessage = f"Failed to load URL: {url}"
                    self.dispatchEvent(error)

            self.dispatchEvent(Event(Event.COMPLETE))
        
        except IOError as e:
            # print(f'IOError: {str(e)}')
            error = ErrorEvent(ErrorEvent.IO_ERROR)
            error.errorMessage = f'IOError: {str(e)}'
            self.dispatchEvent(error)

        except requests.exceptions.SSLError as e:
            # print(f'SecurityError: {str(e)}')
            error = ErrorEvent(ErrorEvent.SECURITY_ERROR)
            error.errorMessage = f'SecurityError: {str(e)}'
            self.dispatchEvent(error)