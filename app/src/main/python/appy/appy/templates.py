from .widgets import ListView, TextView, Button, ImageButton, RelativeLayout, call_general_function, register_widget, elist
from .java import clazz


##############refresh button##############################
def reset_refresh_buttons_if_needed(widget, views):
    for e in views.all():
        if '__refreshing' in e.tag and e.tag.__refreshing:
            e.visibility = clazz.android.view.View().VISIBLE
            e.tag.__refreshing = False

def refresh_button_action(widget, views, on_click, id):
    call_general_function(on_click, widget=widget, views=views)
    btn = None
    try:
        btn = views.find_id(id)
    except KeyError:
        pass
    if btn is not None:
        btn.visibility = clazz.android.view.View().VISIBLE
    btn.tag.__refreshing = False

def refresh_button_click(widget, views, on_click, id, timer_id=None):
    btn = None
    try:
        btn = views.find_id(id)
    except KeyError:
        #disable timer
        if timer_id is not None:
            widget.cancel_timer(timer_id)
    btn.tag.__refreshing = True
    if btn is not None:
        btn.visibility = clazz.android.view.View().INVISIBLE
    widget.post(refresh_button_action, on_click=on_click, id=id)

def refresh_button(on_click, name=None, initial_refresh=None, widget=None, timeout=None, interval=None):
    btn = ImageButton(style='dark_btn_oval_nopad', colorFilter=0xffffffff, width=140, height=140, left=0, bottom=0, imageResource=clazz.android.R.drawable().ic_popup_sync)
    btn.click = (refresh_button_click, dict(on_click=on_click, id=btn.id))
    if name is not None:
        btn.name = name

    btn.tag.__refreshing = False

    if (initial_refresh or interval or timeout) and not widget:
        raise ValueError('must supply widget argument when using initial_refresh, interval or timeout')

    if initial_refresh:
        widget.invoke_click(btn)
    if interval:
        widget.set_interval(interval, widget.click_invoker, element_id=btn.id)
    if timeout:
        widget.set_timeout(timeout, widget.click_invoker, element_id=btn.id)
    return btn

##################background####################################
def background(widget, name=None, color=None, drawable=None):
    if isinstance(color, dict):
        color = widget.color(**color)
    elif isinstance(color, (list, tuple)):
        color = widget.color(*color)
    elif isinstance(color, int):
        color = color
    else:
        color = widget.color(r=0, g=0, b=0, a=100)

    if drawable is None:
        drawable = clazz.com.appy.R.drawable().rounded_rect

    bg = RelativeLayout(width=widget.width, height=widget.height, backgroundResource=drawable)
    bg.backgroundTint = color | 0xff000000
    bg.backgroundAlpha = (color >> 24) & 0xff
    if name is not None:
        bg.name = name
    return bg

##############list template###############################
def call_list_adapter(widget, adapter, value, **kwargs):
    view = elist([TextView(textViewTextSize=(clazz.android.util.TypedValue().COMPLEX_UNIT_SP, 15))])
    if adapter is not None:
        call_general_function(adapter, widget=widget, view=view, value=value, **kwargs)
    else:
        view[0].text = str(value)
    return view

def updating_list_refresh_action(widget, views, on_refresh, adapter, update_hook):
    values = call_general_function(on_refresh, widget=widget, views=views)
    views['list'].children = None if not values else [call_list_adapter(widget, adapter, value=v, index=i) for i, v in enumerate(values)]
    if update_hook is not None:
        update_hook(widget, views)

def updating_list_create(widget, initial_values, on_refresh, background_param, adapter, initial_refresh, timeout, interval, create_hook, update_hook):
    btn = refresh_button((updating_list_refresh_action, dict(on_refresh=on_refresh, adapter=adapter, update_hook=update_hook)), initial_refresh=initial_refresh, widget=widget, timeout=timeout, interval=interval, name='refresh_button')
    lst = ListView(name='list', children=None if not initial_values else [call_list_adapter(widget, adapter, value=v, index=i) for i, v in enumerate(initial_values)])

    views = elist()
    if background_param is not None and background_param is not False:
        views.append(background(widget, color=None if background_param is True else background_param))

    views.append(lst)
    views.append(btn)
    
    if create_hook is not None:
        create_hook(widget, views)
    
    return views

def updating_list(name, initial_values=None, on_refresh=None, background=None, adapter=None, initial_refresh=None, timeout=None, interval=None, create_hook=None, update_hook=None):
    register_widget(name, (updating_list_create, dict(initial_values=initial_values, on_refresh=on_refresh, background_param=background, adapter=adapter, initial_refresh=initial_refresh, timeout=timeout, interval=interval, create_hook=create_hook, update_hook=update_hook)), reset_refresh_buttons_if_needed)

##############text template############################
def call_text_adapter(widget, adapter, value, view, **kwargs):
    if adapter is not None:
        call_general_function(adapter, widget=widget, view=view, value=value, **kwargs)
    else:
        view.text = str(value)

def updating_text_refresh_action(widget, views, on_refresh, adapter, update_hook):
    value = call_general_function(on_refresh, widget=widget, views=views)
    call_text_adapter(widget, adapter, value=value, view=views['content'])
    if update_hook is not None:
        update_hook(widget, views)

def updating_text_create(widget, initial_value, on_refresh, background_param, adapter, initial_refresh, timeout, interval, create_hook, update_hook):
    text = TextView(name='content', text='', textViewTextSize=(clazz.android.util.TypedValue().COMPLEX_UNIT_SP, 30))
    text.left = (widget.width  / 2) - (text.width  / 2)
    text.top  = (widget.height / 2) - (text.height / 2)
    if initial_value is not None:
        call_text_adapter(widget, adapter, value=initial_value, view=text)

    btn = refresh_button((updating_text_refresh_action, dict(on_refresh=on_refresh, adapter=adapter, update_hook=update_hook)), initial_refresh=initial_refresh, widget=widget, timeout=timeout, interval=interval, name='refresh_button')

    views = elist()
    if background_param is not None and background_param is not False:
        views.append(background(widget, color=None if background_param is True else background_param))

    views.append(text)
    views.append(btn)
    
    if create_hook is not None:
        create_hook(widget, views)
        
    return views

def updating_text(name, initial_value=None, on_refresh=None, background=None, adapter=None, initial_refresh=None, timeout=None, interval=None, create_hook=None, update_hook=None):
    register_widget(name, (updating_text_create, dict(initial_value=initial_value, on_refresh=on_refresh, background_param=background, adapter=adapter, initial_refresh=initial_refresh, timeout=timeout, interval=interval, create_hook=create_hook, update_hook=update_hook)), reset_refresh_buttons_if_needed)

#################keyboard###############################
def key_backspace_click(output):
    output.text = output.text[:-1]

def key_click(widget, views, output_id, key=None, handler=None):
    output = views.find_id(output_id)
    if handler is not None:
        call_general_function(handler, widget=widget, output=output)
    else:
        output.text = output.text + key

keyboard_english = ['qwertyuiop',
                    'asdfghjkl',
                    list('zxcvbnm') + [dict(label='←', handler=key_backspace_click)],
                    [dict(label='space', key=' ', width=600, height=150)]]

def keyboard(widget, layout=None):
    if layout is None:
        layout = keyboard_english
    resolved_layout = []
    for line in layout:
        resolved_line = []
        for key_dict in line:
            if isinstance(key_dict, dict):
                key_dict.setdefault('width', 150)
                key_dict.setdefault('height', 150)
            else:
                key_dict = dict(label=key_dict, width=150, height=150)
            resolved_line.append((key_dict, resolved_line[-1][1] + resolved_line[-1][0]['width'] if resolved_line else 0))

        resolved_layout.append((resolved_line, resolved_line[-1][1] + resolved_line[-1][0]['width'], max(x[0]['height'] for x in resolved_line), resolved_layout[-1][3] + resolved_layout[-1][2] if resolved_layout else 0))

    layout_height = resolved_layout[-1][3] + resolved_layout[-1][2]
    btns = []
    edit = TextView(name='output', text='', textViewTextSize=(clazz.android.util.TypedValue().COMPLEX_UNIT_SP, 30))
    for resolved_line in resolved_layout:
        btn_line = []
        line, line_width, line_height, top = resolved_line
        for e in line:
            key_dict, left = e
            btn = Button(style='secondary_btn_nopad',
                         text=key_dict['label'],
                         width=key_dict['width'],
                         height=key_dict['height'],
                         left=((widget.width - line_width) / 2) + left,
                         top=(widget.height - layout_height) + top,
                         )
            if 'handler' in key_dict:
                btn.click = (key_click, dict(handler=key_dict['handler'], output_id=edit.id))
            else:
                btn.click = (key_click, dict(key=key_dict.get('key', key_dict['label']), output_id=edit.id))

            btn_line.append(btn)
        btns.append(btn_line)

    edit.top = btns[0][0].top - edit.height - 10
    return [edit] + [e for l in btns for e in l]
