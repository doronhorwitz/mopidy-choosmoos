class _Proxy(object):
    def __init__(self, proxied_object_name):
        self.proxied_object_name = proxied_object_name

    def __getattr__(self, item):
        return getattr(_proxied_objects[self.proxied_object_name], item)


_proxied_objects = {}


def set_global(proxy_obj, actual_obj):
    _proxied_objects[proxy_obj.proxied_object_name] = actual_obj


def reset_global(proxy_obj):
    _proxied_objects[proxy_obj.proxied_object_name] = None


core = _Proxy('core')
db = _Proxy('db')
buttons = _Proxy('buttons')
rfid = _Proxy('rfid')
spotify_playlist = _Proxy('spotify_playlist')
websocket = _Proxy('websocket')
onboard_leds = _Proxy('onboard_leds')
sound = _Proxy('sound')
