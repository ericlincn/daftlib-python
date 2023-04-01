from cn.daftlib.events.ErrorEvent import ErrorEvent
from cn.daftlib.events.Event import Event
from cn.daftlib.events.ProgressEvent import ProgressEvent
from cn.daftlib.net.ILoadable import ILoadable
from cn.daftlib.events.EventDispatcher import EventDispatcher
import asyncio
import aiohttp
import requests

# Usage:
# import asyncio
# def onComplete(e):
#     l = e.target
#     print("onComplete", l.content, l.url)
# def onProgress(e):
#     print("onProgress", e.percent, str(e.bytesLoaded) + "/" + str(e.bytesTotal))
# async def main():
#     l = AsyncLoader()
#     l.addEventListener(Event.COMPLETE, onComplete)
#     l.addEventListener(ProgressEvent.PROGRESS, onProgress)
#     await l.load("https://www.baidu.com/img/flexible/logo/pc/result.png")
#     # await l.load("https://www.bing.com/search?q=loadable&qs=n&form=QBRE&sp=-1&lq=0&pq=loadable&sc=10-8&sk=&cvid=D203C515419349ABBA755EBDB07ED1D9&ghsh=0&ghacc=0&ghpl=")
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

class AsyncLoader(EventDispatcher, ILoadable):
    
    __content:bytes = None
    __url:str = None
    __response = None

    def __init__(self, target = None) -> None:
        super().__init__(target)

    @property
    def content(self) -> bytes:
        return self.__content
    
    @property
    def url(self) -> str:
        return self.__url
    
    async def load(self, url:str) -> None:

        self.__url = url
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    
                    if response.status == 200:
                        self.__response = response
                        content_length = int(response.headers.get('Content-Length', 0))
                        content = b''
                        async for chunk in response.content.iter_chunked(1024):
                            content += chunk
                            event = ProgressEvent(ProgressEvent.PROGRESS)
                            event.bytesLoaded = len(content)
                            event.bytesTotal = content_length

                            if content_length > 0:
                                # progress = int(len(content) / content_length * 100)
                                # print(f'Loaded {progress}%')
                                event.percent = len(content) / content_length
                            else:
                                event.percent = -1
                            
                            self.dispatchEvent(event)
                        self.__content = content

                    else:
                        # print(f"Failed to load URL: {url}")
                        error = ErrorEvent(ErrorEvent.ERROR)
                        error.errorMessage = f"Failed to load URL: {url}"
                        self.dispatchEvent(error)

            # print('Finished')
            self.dispatchEvent(Event(Event.COMPLETE))

        except IOError as e:
            # print(f'IOError: {str(e)}')
            error = ErrorEvent(ErrorEvent.IO_ERROR)
            error.errorMessage = f'IOError: {str(e)}'
            self.dispatchEvent(error)

        except aiohttp.ClientError as e:
            # print(f'SecurityError: {str(e)}')
            error = ErrorEvent(ErrorEvent.SECURITY_ERROR)
            error.errorMessage = f'SecurityError: {str(e)}'
            self.dispatchEvent(error)

        except requests.exceptions.SSLError as e:
            # print(f'SecurityError: {str(e)}')
            error = ErrorEvent(ErrorEvent.SECURITY_ERROR)
            error.errorMessage = f'SecurityError: {str(e)}'
            self.dispatchEvent(error)

    def cancle(self) -> None:
        if self.__response:
            self.__response.close()

        self.__content = None
        self.__url = None
        self.__response = None