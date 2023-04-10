from cn.daftlib.events.Event import Event
from cn.daftlib.transitions.Tween import Tween
from cn.daftlib.time.EnterFrame import EnterFrame

# Usage:
# class A:
#     v:float=2
# a = A()
# def onUpdate():
#     print(a.v)
# def onComplete(first, second):
#     print("complete", first, second)
# pulse = EnterFrame()
# TweenManager.setPulseTarget(pulse)
# TweenManager.tweenTo(a, 2, {"v":0, "onUpdate":onUpdate, "onComplete":onComplete, "onCompleteParams":[1024, 2048], "ease":Easing.backEaseInOut})
# TweenManager.delayCall(4, onComplete, ["big", "small"])

class TweenManager:

    __tweenMap:dict[Tween] = {}
    __pulseTarget:EnterFrame = None

    @staticmethod
    def setPulseTarget(pulseTarget:EnterFrame):
        TweenManager.__pulseTarget = pulseTarget

    @staticmethod
    def tweenTo(target, duration, vars):
        oldTween:Tween = TweenManager.__tweenMap.get(target)
        newTween:Tween = Tween(target, duration, vars)

        if oldTween != None:
            TweenManager.__pulseTarget.removeEventListener(Event.ENTER_FRAME, oldTween.render)
            oldTween.destroy()
            oldTween = None
            del TweenManager.__tweenMap[target]

        # newTween.start()
        TweenManager.__pulseTarget.addEventListener(Event.ENTER_FRAME, newTween.render)
        TweenManager.__tweenMap[target] = newTween

    @staticmethod
    def tweenFrom(target, duration, vars):
        oldTween:Tween = TweenManager.__tweenMap.get(target)
        newTween:Tween = Tween(target, duration, vars, True)

        if oldTween != None:
            TweenManager.__pulseTarget.removeEventListener(Event.ENTER_FRAME, oldTween.render)
            oldTween.destroy()
            oldTween = None
            del TweenManager.__tweenMap[target]

        # newTween.start()
        TweenManager.__pulseTarget.addEventListener(Event.ENTER_FRAME, newTween.render)
        TweenManager.__tweenMap[target] = newTween

    @staticmethod
    def delayCall(delay, func, funcParams = None):
        oldTween:Tween = TweenManager.__tweenMap.get(func)
        newTween:Tween = Tween(func, 0, {'delay':delay, 'onComplete':func, 'onCompleteParams':funcParams})

        if oldTween != None:
            TweenManager.__pulseTarget.removeEventListener(Event.ENTER_FRAME, oldTween.render)
            oldTween.destroy()
            oldTween = None
            del TweenManager.__tweenMap[func]

        # newTween.start()
        TweenManager.__pulseTarget.addEventListener(Event.ENTER_FRAME, newTween.render)
        TweenManager.__tweenMap[func] = newTween

    @staticmethod
    def removeTweenForTarget(target):
        oldTween:Tween = TweenManager.__tweenMap.get(target)

        if oldTween != None:
            TweenManager.__pulseTarget.removeEventListener(Event.ENTER_FRAME, oldTween.render)
            oldTween.destroy()
            oldTween = None
            del TweenManager.__tweenMap[target]

    @staticmethod
    def removeDelayCallForMethod(func):
        TweenManager.removeTweenForTarget(func)

    @staticmethod
    def removeAllTween():
        for key in TweenManager.__tweenMap:
            TweenManager.removeTweenForTarget(key)
        TweenManager.__tweenMap = {}