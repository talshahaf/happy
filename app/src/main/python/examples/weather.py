import json, requests, datetime, io
from xml.etree import ElementTree as ET
from appy.widgets import register_widget, ImageView, TextView, AttributeFunction
from appy.templates import background, refresh_button, reset_refresh_buttons_if_needed
from appy import widgets, java

# inaccurate location is enough
PERMISSION = 'ACCESS_COARSE_LOCATION'

# get location using the android providers (currently unused by this widget)
def get_location():
    # request_permissions blocks until user action
    # request_permissions returns a tuple: (granted, denied)
    if PERMISSION not in widgets.request_permissions(PERMISSION)[0]:
        print('no perms')
        return None
    # getLastKnownLocation instead of active location request
    locationManager = widgets.java_context().getSystemService(java.clazz.android.content.Context().LOCATION_SERVICE);
    lastKnownLocation = locationManager.getLastKnownLocation(java.clazz.android.location.LocationManager().NETWORK_PROVIDER);
    if lastKnownLocation == java.Null:
        print('no loc')
        return None
    return dict(lat=float(lastKnownLocation.getLatitude()),
                lon=float(lastKnownLocation.getLongitude()),
                acc=float(lastKnownLocation.getAccuracy()))

# see https://api.met.no/
FORECAST = 'https://api.met.no/weatherapi/locationforecast/1.9/?lat={lat:.2f}&lon={lon:.2f}'
SUNRISE = 'https://api.met.no/weatherapi/sunrise/1.1/?lat={lat:.2f}&lon={lon:.2f}&date={date}'
WEATHER_ICONS = 'https://api.met.no/weatherapi/weathericon/1.1/?symbol={symbol}&is_night={night}&content_type=image/png'

# large responses might be trimmed using the simple requests api
def large_get(url):
    buf = io.BytesIO()
    r = requests.get(url, stream=True, timeout=60)
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            buf.write(chunk)
    return buf.getvalue()
    
def namespaces(xml):
    return dict([node for _, node in ET.iterparse(io.StringIO(xml), events=['start-ns'])])

def read_xml(url):
    xml = large_get(url).decode()
    return ET.fromstring(xml), namespaces(xml)
    
def parse_date(datestr):
    return datetime.datetime.strptime(datestr.translate({ord(':'): None, ord('-'): None}), "%Y%m%dT%H%M%SZ").replace(tzinfo=datetime.timezone.utc)
    
def isnight(utcdate, lat, lon):
    utcdate = utcdate.replace(tzinfo=datetime.timezone.utc)
    root, namespaces = read_xml(SUNRISE.format(date=utcdate.strftime('%Y-%m-%d'), lat=lat, lon=lon))
    sun = root.find('time').find('location').find('sun')
    never_rise, never_set = sun.get('never_rise'), sun.get('never_set')
    rise, set = parse_date(sun.get('rise')) if 'rise' in sun.attrib else None, parse_date(sun.get('set')) if 'set' in sun.attrib else None
    if never_rise:
        return True
    elif never_set:
        return False
    return utcdate < rise or utcdate > set        

def forecast(utcdate, lat, lon):
    root, namespaces = read_xml(FORECAST.format(lat=lat, lon=lon))
    utcdate = utcdate.replace(minute=0, second=0, microsecond=0, tzinfo=datetime.timezone.utc)
    times = root.find('product').findall('time')
    temp = times[0].find('location').find('temperature')
    symbol = times[1].find('location').find('symbol')
    return temp.get('unit'), temp.get('value'), symbol.get('number')

def on_refresh(widget, views):
    try:
        date = datetime.datetime.utcnow()
        lat, lon = widget.config.lat, widget.config.lon
        unit, temp, symbol = forecast(date, lat=lat, lon=lon)
        night = isnight(date, lat=lat, lon=lon)
        icon = WEATHER_ICONS.format(symbol=symbol, night=1 if night else 0)
        
        views['temp'].text = f'{temp}°{unit[0].upper()}'
        views['img'].imageURI = widgets.file_uri(widgets.download_resource(icon))
    except OSError:
        print('error fetching information')
    
def create(widget):
    bg = background()
    refresh = refresh_button(on_refresh, widget=widget, initial_refresh=True, interval=4*3600)
    # moving refresh button
    del refresh.left
    refresh.right = 0
    #                               width and height are 60% of the widget's height but no more than 200 pixels 
    img = ImageView(name='img', width=AttributeFunction.min(200, widget.height * 0.6), height=AttributeFunction.min(200, widget.height * 0.6), adjustViewBounds=True, hcenter=widget.hcenter, top=10)
    text = TextView(name='temp', top=img.ibottom, hcenter=widget.hcenter, textColor=0xb3ffffff, textSize=30)
    # bg is first
    return [bg, img, text, refresh]
    
# no custom update callback is needed, just recover refresh button on error,    location is configurable in configurations tab
register_widget('weather', create, reset_refresh_buttons_if_needed, config=dict(lat=32.08, lon=34.78))