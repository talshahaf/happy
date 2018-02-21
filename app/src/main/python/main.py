import random

from widgets import Button, TextView, ListView, register_widget, pip_install
from java import clazz

#=========================================================================
def example_on_create(widget_id):
    txt = TextView(text='zxc', textViewTextSize=(clazz.android.util.TypedValue().COMPLEX_UNIT_SP, 30), click=lambda e: setattr(e, 'text', str(random.randint(50, 60))))
    lst = ListView(children=[
        txt,
        txt.duplicate()
    ])
    return lst

def example2_on_create(widget_id):
    return [
            Button(text='ref', textViewTextSize=(clazz.android.util.TypedValue().COMPLEX_UNIT_SP, 30), click=lambda e: None),
            TextView(text='bbb', textViewTextSize=(clazz.android.util.TypedValue().COMPLEX_UNIT_SP, 30))
        ]

def logcat_on_create(widget_id):
    return ListView(children=[TextView(text='ready...', textViewTextSize=(clazz.android.util.TypedValue().COMPLEX_UNIT_SP, 15), click=lambda e: None)])

i = 1
def logcat_on_update(widget_id, views):
    global i
    btn = Button(text='ref', textViewTextSize=(clazz.android.util.TypedValue().COMPLEX_UNIT_SP, 30), click=lambda e: None)
    lst = ListView(children=[TextView(text=str(random.randint(300, 400)), textViewTextSize=(clazz.android.util.TypedValue().COMPLEX_UNIT_SP, 15), click=lambda e: None) for _ in range(i)])

    btn.top = 400
    lst.top = btn.top / 2

    i += 1
    return [btn, lst]

def newwidget_on_create(widget_id):
    return None

def newwidget_on_update(widget_id, views):
    print(views)

#register_widget('example', example_on_create, None)
#register_widget('example2', example2_on_create, None)
register_widget('logcat', logcat_on_create, logcat_on_update)

#TODO fix bytes serialization