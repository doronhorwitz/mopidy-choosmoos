from .globals import core
from .utils.pn7150 import PN7150


class RFID(object):

    def __init__(self, nfc_demo_app_location=None):
        self._pn7150 = PN7150(nfc_demo_app_location)

    def start_play_mode(self):
        self._pn7150.when_tag_read = self._load_playlist
        self._pn7150.start_reading()

    def write(self, text):
        return self._pn7150.write(text)

    def read_once(self):
        return self._pn7150.read_once()

    def stop_reading(self):
        self._pn7150.stop_reading()

    def start_reading(self):
        self._pn7150.start_reading()

    @staticmethod
    def _load_playlist(playlist_id):
        core.load_playlist(playlist_id)
