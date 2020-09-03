class _Proxy:
    def __init__(self, proxied_object_name):
        self.proxied_object_name = proxied_object_name

    def __getattr__(self, item):
        return getattr(_proxied_objects[self.proxied_object_name], item)


_proxied_objects = {}


def set_global(proxy_obj, actual_obj):
    _proxied_objects[proxy_obj.proxied_object_name] = actual_obj


logger = _Proxy("logger")
mopidy_core = _Proxy("mopidy_core")
db = _Proxy("db")
buttons = _Proxy("buttons")
rfid = _Proxy("rfid")
spotify_playlist = _Proxy("spotify_playlist")
mopidy_web = _Proxy("mopidy_web")
onboard_leds = _Proxy("onboard_leds")
sound = _Proxy("sound")
