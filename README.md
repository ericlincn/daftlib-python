[![Apache 2.0 License](https://img.shields.io/badge/license-Apache-blue.svg?style=flat)](LICENSE.md)

# daftlib-python
一系列常用的工具类及数据结构集合
A collection of commonly used utility classes and data structures.

## Features
- RGB与HSL色彩空间的相互转换 Conversion between RGB and HSL color spaces
- 基于事件或基于观察者模式的消息传递机制 Message passing mechanism based on event or observer pattern
- 自动弹性布局 Automatic responsive layout
- 外部资源的队列化读取 Queued loading of external resources
- 多点触摸的实现 Implementation of multitouch
- 缓动的实现 Implementation of easing functions
- 以及其他 And others.

## Usage Example
Conversion between color spaces
```python
rgb = RGB(23, 255, 7)
hsl = HSL(120, .5, .3)
print(hex(rgb.value), hex(hsl.value))

hsl.value = rgb.value
print(hex(hsl.value), ColorUtil.getDifference(hsl.value, rgb.value))
```

Event system
```python
def onComplete(e):
    print("complete", e)
    
def onComplete2(e):
    print("complete2", e)
    
def onActive(e):
    print("active", e)
    
dispatcher = EventDispatcher()
dispatcher.addEventListener(Event.COMPLETE, onComplete)
dispatcher.addEventListener(Event.ACTIVATE, onActive)
dispatcher.addEventListener(Event.COMPLETE, onComplete2)
dispatcher.addEventListener(Event.ACTIVATE, onComplete2)
dispatcher.dispatchEvent(Event(Event.COMPLETE))
dispatcher.dispatchEvent(Event(Event.ACTIVATE))
dispatcher.dispatchEvent(Event(Event.COMPLETE))

print("Try to remove some listeners...")
dispatcher.removeEventListenersForListener(onComplete2)
dispatcher.removeEventListenersForType(Event.COMPLETE)
dispatcher.dispatchEvent(Event(Event.COMPLETE))
dispatcher.dispatchEvent(Event(Event.ACTIVATE))
dispatcher.dispatchEvent(Event(Event.COMPLETE))

dispatcher.removeAllEventListeners()
```

## Requirements
- requests
- aiohttp
