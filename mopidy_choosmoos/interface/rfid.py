from uuid import uuid4

from contextlib import contextmanager

from ..globals import mopidy_core, db, onboard_leds, mopidy_web
from ..utils import validate_uuid4
from ..utils.pn7150 import PN7150

_DEFAULT_NFC_DEMO_APP_LOCATION = "/home/pi/linux_libnfc-nci-master"


class RFID:
    def __init__(self, nfc_demo_app_location=None):
        self._pn7150 = (
            PN7150(nfc_demo_app_location)
            if nfc_demo_app_location
            else PN7150(_DEFAULT_NFC_DEMO_APP_LOCATION)
        )
        self._pn7150.when_tag_read = self._load_playlist

    def _initialize_tag(self):
        existing_text = self._pn7150.read_once(wait_for_tag_removal=False)

        if validate_uuid4(existing_text):
            return existing_text
        else:
            new_uuid = str(uuid4())
            write_success = self._pn7150.write(new_uuid, wait_for_tag_removal=False)
            return new_uuid if write_success else None

    @contextmanager
    def _temporarily_stop_reading_and_initialize_tag(self):
        self.stop_reading()
        onboard_leds.on("pwr")

        yield self._initialize_tag()

        onboard_leds.off("pwr")
        self.start_reading()

    def assign_tag_to_playlist(self, playlist_uri):
        mopidy_web.send_tag_write_ready(playlist_uri)
        with self._temporarily_stop_reading_and_initialize_tag() as tag_uuid:
            if tag_uuid:
                db.assign_playlist_uri_to_tag_uuid(tag_uuid, playlist_uri)
                mopidy_web.send_tag_assign_success(playlist_uri, tag_uuid)
            else:
                mopidy_web.send_tag_assign_failure(playlist_uri)

    def stop_reading(self):
        self._pn7150.stop_reading()

    def start_reading(self):
        self._pn7150.start_reading()

    @staticmethod
    def _load_playlist(tag_uuid):
        mopidy_core.load_playlist(tag_uuid)
