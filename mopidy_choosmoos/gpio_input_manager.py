import logging
import mem
from gpiozero import Button
from .pn7150 import PN7150

logger = logging.getLogger(__name__)


class GPIOManager(object):

    BUTTON_TO_BCM_LOOKUP = {
        1: 5,
        2: 6,
        3: 12,
        4: 13,
        5: 16,
        6: 26,
    }

    def __init__(self, frontend, next_pin_number=None, previous_pin_number=None, volume_up_pin_number=None,
                 volume_down_pin_number=None, play_pause_pin_number=None, nfc_demo_app_location=None):
        self._frontend = frontend

        if next_pin_number:
            print('next_pin_number: {}'.format(next_pin_number))
            self._next_button = Button(self.BUTTON_TO_BCM_LOOKUP[next_pin_number])
            self._next_button.when_pressed = self._next
        if previous_pin_number:
            print('previous_pin_number: {}'.format(previous_pin_number))
            self._previous_button = Button(self.BUTTON_TO_BCM_LOOKUP[previous_pin_number])
            self._previous_button.when_pressed = self._previous
        if volume_up_pin_number:
            print('volume_up_pin_number: {}'.format(volume_up_pin_number))
            self._volume_up_button = Button(self.BUTTON_TO_BCM_LOOKUP[volume_up_pin_number])
            self._volume_up_button.when_pressed = self._volume_up
        if volume_down_pin_number:
            print('volume_down_pin_number: {}'.format(volume_down_pin_number))
            self._volume_down_button = Button(self.BUTTON_TO_BCM_LOOKUP[volume_down_pin_number])
            self._volume_down_button.when_pressed = self._volume_down
            self._volume_down_button.when_held = self._mute
        if play_pause_pin_number:
            print('play_pause_pin_number: {}'.format(play_pause_pin_number))
            self._play_pause_button = Button(self.BUTTON_TO_BCM_LOOKUP[play_pause_pin_number])
            self._play_pause_button.when_pressed = self._play_pause

        pn7150 = PN7150(nfc_demo_app_location) if nfc_demo_app_location else PN7150()
        pn7150.when_tag_read = self._load_playlist
        pn7150.start_reading()

        mem.message_bus.set_pn7150(pn7150)

    def stop(self):
        mem.message_bus.pn7150_stop_reading()

    def _next(self):
        self._frontend.input('next')

    def _previous(self):
        self._frontend.input('previous')

    def _volume_up(self):
        self._frontend.input('volume_up')

    def _volume_down(self):
        self._frontend.input('volume_down')

    def _play_pause(self):
        self._frontend.input('play_pause')

    def _mute(self):
        self._frontend.input('mute')

    def _load_playlist(self, playlist_id):
        self._frontend.input('load_playlist', playlist_id=playlist_id)
