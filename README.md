[![Apache 2.0 License](https://img.shields.io/badge/license-Apache-blue.svg?style=flat)](LICENSE.md)

# daftlib-python
A collection of commonly used utility classes and data structures.

## Features
- Conversion between RGB and HSL color spaces
- Message passing mechanism based on event or observer pattern
- Automatic responsive layout
- Queued loading of external resources
- Implementation of multitouch
- Implementation of easing functions
- And others.

## Requirements
- requests
- aiohttp

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


