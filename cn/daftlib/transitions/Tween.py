from cn.daftlib.core.IDestroyable import IDestroyable
import cn.daftlib.transitions.TweenManager as tm
import time

class Tween(IDestroyable):

    def __init__(self, target, duration:float, vars:dict, reverse:bool = False) -> None:

        self.__target = target

        # Easing equations don't work when the duration is zero.
        self.__duration = duration or 0.001
        self.__duration = max(0.001, duration) * 1000
        self.__vars = vars
        self.__ease = vars.get('ease') or Tween.__easeOut
        self.__delay = vars.get('delay') or 0
        self.__delay = max(0, self.__delay) * 1000
        self.__reverse = reverse
        self.__onComplete = vars.get('onComplete') or None
        self.__onCompleteParams = vars.get('onCompleteParams') or None
        self.__onUpdate = vars.get('onUpdate') or None
        self.__onUpdateParams = vars.get('onUpdateParams') or None

        self.__tweenInfoArr = []
        self.__startTime = None

        self.__initTweenInfo()

    def destroy(self) -> None:
        self.__target = None
        self.__vars = None
        self.__ease = None
        self.__onComplete = None
        self.__onCompleteParams = None
        self.__onUpdate = None
        self.__onUpdateParams = None
        self.__tweenInfoArr = None

    def __str__(self) -> str:
        return f"[{str(self.__class__)[8:-2]}](duration={self.__duration}, delay={self.__delay}, reverse={self.__reverse})"

    def __initTweenInfo(self) -> None:
        for property in self.__vars:
            #check property is invaild
            if hasattr(self.__target, property):
                self.__tweenInfoArr.append(TweenInfo(self.__target, property, getattr(self.__target, property), self.__vars[property] - getattr(self.__target, property)))

        if self.__reverse == True:
            i = len(self.__tweenInfoArr)
            while i > 0:
                i -= 1
                ti:TweenInfo = self.__tweenInfoArr[i]
                ti.start += ti.change
                ti.change *= -1

                #render at beginning, because __duration is always forced to be at least 0.001 since easing equations can't handle zero.
                setattr(ti.target, ti.property, ti.start)

    def render(self, e) -> None:
        #for destroy fix
        if self.__tweenInfoArr is None:
            return

        #time related
        # if self.__startTime is None:
        #     self.__startTime = getTimer() + self.__delay
        # currentTime = getTimer() - self.__startTime
        if self.__startTime is None:
            self.__startTime = time.perf_counter() * 1000 + self.__delay
        currentTime = time.perf_counter() * 1000 - self.__startTime

        #calculate factor
        factor = 1
        if currentTime < 0:
            #for delay
            factor = 0
        elif currentTime >= self.__duration:
            #for complete
            currentTime = self.__duration
        else:
            factor = self.__ease(currentTime, 0, 1, self.__duration)

        #Tween the property
        i = len(self.__tweenInfoArr)
        while i > 0:
            i -= 1
            ti:TweenInfo = self.__tweenInfoArr[i]
            targetValue = ti.start + factor * ti.change
            setattr(ti.target, ti.property, targetValue)

        #on Update method
        if self.__onUpdate is not None:
            self.__onUpdate() if self.__onUpdateParams is None else self.__onUpdate(*self.__onUpdateParams)

        #on Complete
        if currentTime == self.__duration:
            if self.__onComplete is not None:
                self.__onComplete() if self.__onCompleteParams is None else self.__onComplete(*self.__onCompleteParams)
            
            tm.TweenManager.removeTweenForTarget(self.__target)

    @staticmethod
    def __easeOut(t, b, c, d):
        t = 1 - (t / d)
        return 1 - t * t

class TweenInfo:
    def __init__(self, t, p, s, c) -> None:
        self.target = t
        self.property = p
        self.start = s
        self.change = c