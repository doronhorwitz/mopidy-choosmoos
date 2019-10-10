import logging
from gpiozero import Button

from .globals import core

logger = logging.getLogger(__name__)

BUTTON_NAMES = ('next', 'previous', 'volume_up', 'volume_down', 'play_pause')
_BUTTON_TO_BCM_LOOKUP = {
    1: 5,
    2: 6,
    3: 12,
    4: 13,
    5: 16,
    6: 26,
}


class Buttons(object):

    def __init__(self, next_pin_number=None, previous_pin_number=None, volume_up_pin_number=None,
                 volume_down_pin_number=None, play_pause_pin_number=None,):
        self._next_button = next_pin_number
        self._previous_button = previous_pin_number
        self._volume_up_button = volume_up_pin_number
        self._volume_down_button = volume_down_pin_number
        self._play_pause_button = play_pause_pin_number

        self._create_buttons()

    def _create_buttons(self):
        for button_name in BUTTON_NAMES:
            pin_number = getattr(self, '_{}_button'.format(button_name))
            if pin_number is not None:
                button = Button(_BUTTON_TO_BCM_LOOKUP[pin_number])
                button.when_pressed = getattr(self, '_{}'.format(button_name))

        # To mute, the "volume down" button is held
        if self._volume_down_button:
            self._volume_down_button.when_held = self._mute

    @staticmethod
    def _next():
        core.next()

    @staticmethod
    def _previous():
        core.previous()

    @staticmethod
    def _volume_up():
        core.volume_up()

    @staticmethod
    def _volume_down():
        core.volume_down()

    @staticmethod
    def _play_pause():
        core.play_pause()

    @staticmethod
    def _mute():
        core.mute()
