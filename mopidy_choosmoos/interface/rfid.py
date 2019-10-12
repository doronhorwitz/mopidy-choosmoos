from ..globals import core, onboard_leds
from ..utils.pn7150 import PN7150

_DEFAULT_NFC_DEMO_APP_LOCATION = '/home/pi/linux_libnfc-nci-master'


class RFID(object):

    def __init__(self, nfc_demo_app_location=None):
        self._pn7150 = (
            PN7150(nfc_demo_app_location) if nfc_demo_app_location else PN7150(_DEFAULT_NFC_DEMO_APP_LOCATION))
        self._pn7150.when_tag_read = self._load_playlist

    def write(self, text, wait_for_tag_removal=True):
        return self._pn7150.write(text, wait_for_tag_removal=wait_for_tag_removal)

    def read_once(self, wait_for_tag_removal=True):
        return self._pn7150.read_once(wait_for_tag_removal=wait_for_tag_removal)

    def stop_reading(self):
        self._pn7150.stop_reading()

    def start_reading(self):
        self._pn7150.start_reading()

    @staticmethod
    def _load_playlist(tag_uuid):
        # the response time of the on-board LEDs is slow enough that calling on() and then off() immediately after shows
        # a nice visible blink
        onboard_leds.on('act')
        onboard_leds.off('act')

        core.load_playlist(tag_uuid)
