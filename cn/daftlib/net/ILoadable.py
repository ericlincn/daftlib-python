class ILoadable:

    @property
    def content(self) -> bytes:
        pass
    
    @property
    def url(self) -> str:
        pass

    def load(self, url:str) -> None:
        pass