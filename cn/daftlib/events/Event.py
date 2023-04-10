from cn.daftlib.events.EventPhase import EventPhase

class Event:

    # Events
    ACTIVATE:str = "activate"
    ADDED:str = "added"
    ADDED_TO_STAGE:str = "addedToStage"
    CANCEL:str = "cancel"
    CHANGE:str = "change"
    CLEAR:str = "clear"
    CLOSE:str = "close"
    COMPLETE:str = "complete"
    CONNECT:str = "connect"
    CONTEXT3D_CREATE:str = "context3DCreate"
    COPY:str = "copy"
    CUT:str = "cut"
    DEACTIVATE:str = "deactivate"
    ENTER_FRAME:str = "enterFrame"
    EXIT_FRAME:str = "exitFrame"
    FRAME_CONSTRUCTED:str = "frameConstructed"
    FRAME_LABEL:str = "frameLabel"
    FULLSCREEN:str = "fullScreen"
    ID3:str = "id3"
    INIT:str = "init"
    MOUSE_LEAVE:str = "mouseLeave"
    OPEN:str = "open"
    PASTE:str = "paste"
    REMOVED:str = "removed"
    REMOVED_FROM_STAGE:str = "removedFromStage"
    RENDER:str = "render"
    RESIZE:str = "resize"
    SCROLL:str = "scroll"
    SELECT:str = "select"
    SELECT_ALL:str = "selectAll"
    SOUND_COMPLETE:str = "soundComplete"
    TAB_CHILDREN_CHANGE:str = "tabChildrenChange"
    TAB_ENABLED_CHANGE:str = "tabEnabledChange"
    TAB_INDEX_CHANGE:str = "tabIndexChange"
    TEXTURE_READY:str = "textureReady"
    TEXT_INTERACTION_MODE_CHANGE:str = "textInteractionModeChange"
    UNLOAD:str = "unload"

    # public members
    type:str
    bubbles:bool
    cancelable:bool

    eventPhase:EventPhase
    currentTarget:object
    target:object

    # private members
    __isCanceled:bool
    __isCanceledNow:bool
    __preventDefault:bool

    def __init__(self, type:str, bubbles:bool = False, cancelable:bool = False) -> None:
        
        self.type = type
        self.bubbles = bubbles
        self.cancelable = cancelable

        self.eventPhase = EventPhase.AT_TARGET
        self.currentTarget = None
        self.target = None

        self.__isCanceled = False
        self.__isCanceledNow = False
        self.__preventDefault = False

    def __str__(self) -> str:
        return f"[{str(self.__class__)[8:-2]}](type={self.type}, bubbles={self.bubbles}, cancelable={self.cancelable})"

    # def clone(self) -> Event:
    def clone(self):

        event = Event(self.type, self.bubbles, self.cancelable)
        event.eventPhase = self.eventPhase
        event.target = self.target
        event.currentTarget = self.currentTarget
        return event

    def isDefaultPrevented(self) -> bool:

        return self.__preventDefault

    def preventDefault(self) -> None:

        if self.cancelable:
            self.__preventDefault = True

    def stopImmediatePropagation(self) -> None:

        self.__isCanceled = True
        self.__isCanceledNow = True

    def stopPropagation(self) -> None:

        self.__isCanceled = True

    def isCanceled(self) -> bool:
        return self.__isCanceled
    def isCanceledNow(self) -> bool:
        return self.__isCanceledNow