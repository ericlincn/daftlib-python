[![Apache 2.0 License](https://img.shields.io/badge/license-Apache-blue.svg?style=flat)](LICENSE.md)

# daftlib-python
A collection of commonly used utility classes and data structures.

## Features
- Conversion between RGB and HSL color spaces
- Message passing mechanism based on event or observer pattern
- Queued loading of external resources
- Implementation of easing functions
- And much more.

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

ChatGPT API
```python
llm = OpenAI(api_key)
llm.temperature = 0
prompt = f"With programming language python, the keywords for classes and methods are [class, def], with programming language {target_lang}, the keywords for classes and methods are"
ends = "."
res = llm.completion(prompt, ends)
text = json.loads(res)['choices'][0]['text']
```

Event system
```python
def onComplete(e):
    print("complete", e)
    
def onActive(e):
    print("active", e)
    
dispatcher = EventDispatcher()
dispatcher.addEventListener(Event.COMPLETE, onComplete)
dispatcher.addEventListener(Event.ACTIVATE, onActive)

dispatcher.dispatchEvent(Event(Event.COMPLETE))
dispatcher.dispatchEvent(Event(Event.ACTIVATE))

dispatcher.removeEventListenersForListener(onComplete)
dispatcher.removeEventListenersForType(Event.ACTIVATE)
dispatcher.removeAllEventListeners()
```

Signal system
```python
def onComplete():
    print("complete")
def onActive(data):
    print("active", data)
class B:
    active:Signal = Signal()
    complete:Signal = Signal()

dispathcer = B()
dispathcer.complete.connect(onComplete)
dispathcer.active.connect(onActive)
dispathcer.complete.emit()
dispathcer.active.emit([1,2,3])
dispathcer.complete.disconnectAll()
```

Observer
```python
class Ob(IObserver):
    def notificationHandler(self, notification) -> None:
        print("Got notification:", notification, notification.body)

ob = Ob()
NotificationsCenter.register("noti_name", ob)

# somewhere else ...

NotificationsCenter.sendNotification("noti_name", {"name":"eric"})
```

Queue commands
```python
class Command(EventDispatcher, ICommand):
    def __init__(self) -> None:
        super().__init__()
    def execute(self):
        print(self.extra)
        self.dispatchEvent(Event(Event.COMPLETE))

def completeHandler(e): print("finished")

exe = Executer()
i = 0
while i < 190:
    command = Command()
    command.extra = i
    exe.addCommmand(command)
    i += 1

exe.addEventListener(Event.COMPLETE, completeHandler)
exe.run()
```

Async loader
```python
import asyncio

def onComplete(e):
    l = e.target
    print("onComplete", l.content, l.url)

def onProgress(e):
    print("onProgress", e.percent, str(e.bytesLoaded) + "/" + str(e.bytesTotal))

async def main():
    l = AsyncLoader()
    l.addEventListener(Event.COMPLETE, onComplete)
    l.addEventListener(ProgressEvent.PROGRESS, onProgress)
    await l.load("res://result.png")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

Queue loader
```python
def onComplete(e):
    print("finished")
    ql:QueueLoader = e.target
    print(ql.get('res://result.png'))
   
def onProgress(e):
    print(e.percent, e.bytesLoaded, e.bytesTotal)

ql = QueueLoader()
ql.add('res://splash.png')
ql.add('res://main.png')
ql.add('res://result.png')
ql.addEventListener(Event.COMPLETE, onComplete)
ql.addEventListener(ProgressEvent.PROGRESS, onProgress)
ql.start()
```

Pulse
```python
def onEnterFrame(e):
    print(e)
pulse = EnterFrame(fps=60)
pulse.addEventListener(Event.ENTER_FRAME, onEnterFrame)
```

Tween & Delay call
```python
class A: v:float=2
a = A()

def onUpdate():
    print(a.v)

def onComplete(first, second):
    print("complete", first, second)

pulse = EnterFrame()
TweenManager.setPulseTarget(pulse)
TweenManager.tweenTo(a, 2, {"v":0, "onUpdate":onUpdate, "onComplete":onComplete, "onCompleteParams":[1024, 2048], "ease":Easing.backEaseInOut})

TweenManager.delayCall(4, onComplete, ["big", "small"])
```

SQLAlchemy with auto commit. Require Flask, Flask-SQLAlchemy
```python
app = Flask(__name__)
db = FlaskSQLAlchemy(app)

@app.route('/example')
def example():
    with db.auto_commit():
        # Perform database operations here, For example, adding a new record:
        new_record = YourModel(name='example', value=123)
        db.session.add(new_record)
# The changes will be automatically committed at the end of the with-block if no exceptions occurred.
return 'Transaction completed!'
```

Create Table at runtime. Useful when it's necessary to sharding at runtime. Require Flask, Flask-SQLAlchemy
```python
app = Flask(__name__)
db = FlaskSQLAlchemy(app)

@app.route('/example')
def example():
    _dict = {
        'id': db.Column(db.Integer, primary_key = True, autoincrement = True),
        'type': db.Column(db.String(20), nullable = False),
        'create_time': db.Column(db.DateTime, default = datetime.now)
    }
    data_model = RuntimeModel.model(db, "data_0", _dict)
    if not db.has_table(data_model.tablename):
        db.create_table(data_model)
return 'Table created!'
```
***Be cautious!!! Using Flask-Migrate could accidentally delete runtime tables that have already been created. To address this issue, modify the def run_migrations_online(): function in the env.py file located in the migrations folder:***
```python
connectable = get_engine()
target_metadata = get_metadata()
target_metadata.reflect(get_engine(), only=["data_0"])

with connectable.connect() as connection:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        process_revision_directives=process_revision_directives,
        **current_app.extensions['migrate'].configure_args
    )

    with context.begin_transaction():
        context.run_migrations()
```

When using htmx, ignore specific status codes in certain responses, such as 422 and 429, while maintaining htmx's default swap behavior. Require Flask, htmx
```html
<!-- html code in Jinja2 template-->
{{ htmx_script | safe }}

<input type="email" id="email" name="email" required
    hx-get="/captcha/email"
    hx-on="htmx:beforeOnLoad: before_on_load(event)">
```

```python
@app.route('/register')
def register():
    return render_template("register.html", htmx_script = Js.htmx_ignore_error([422, 429]))
```

Generate Snowflake ID
```python
machine_id = 23
generator = SnowflakeID(machine_id)

for _ in range(10):
    unique_id = generator.generate_id()
    print(unique_id)
```
