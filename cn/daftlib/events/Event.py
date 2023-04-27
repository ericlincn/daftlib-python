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
    target:object

    def __init__(self, type:str) -> None:
        
        self.type = type
        self.target = None

    def __str__(self) -> str:
        return f"[{str(self.__class__)[8:-2]}](type={self.type})"

    # def clone(self) -> Event:
    def clone(self):

        event = Event(self.type)
        event.target = self.target
        return event