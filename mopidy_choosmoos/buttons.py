import logging
from gpiozero import Button

from .globals import core

logger = logging.getLogger(__name__)


class Buttons(object):

    BUTTON_TO_BCM_LOOKUP = {
        1: 5,
        2: 6,
        3: 12,
        4: 13,
        5: 16,
        6: 26,
    }

    def __init__(self, next_pin_number=None, previous_pin_number=None, volume_up_pin_number=None,
                 volume_down_pin_number=None, play_pause_pin_number=None,):
        self._next_button = None
        self._previous_button = None
        self._volume_up_button = None
        self._volume_down_button = None
        self._play_pause_button = None

        pin_number_lookup = {
            'next': next_pin_number,
            'previous': previous_pin_number,
            'volume_up': volume_up_pin_number,
            'volume_down': volume_down_pin_number,
            'play_pause': play_pause_pin_number,
        }

        for button_name, pin_nummber in pin_number_lookup.iteritems():
            if pin_nummber is not None:
                button = Button(self.BUTTON_TO_BCM_LOOKUP[pin_nummber])
                button.when_pressed = getattr(self, '_{}'.format(button_name))
                setattr(self, '_{}_button'.format(button_name), button)

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
