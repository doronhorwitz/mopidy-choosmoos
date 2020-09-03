import logging
from gpiozero import Button

from ..globals import mopidy_core, onboard_leds, sound

logger = logging.getLogger(__name__)


BUTTON_NAMES = ("next", "previous", "volume_up", "volume_down", "play_pause")
_BUTTON_TO_BCM_LOOKUP = {
    1: 5,
    2: 6,
    3: 12,
    4: 13,
    5: 16,
    6: 26,
}


class Buttons:
    def __init__(
        self,
        next_pin_number=None,
        previous_pin_number=None,
        volume_up_pin_number=None,
        volume_down_pin_number=None,
        play_pause_pin_number=None,
    ):
        self._next_button = next_pin_number
        self._previous_button = previous_pin_number
        self._volume_up_button = volume_up_pin_number
        self._volume_down_button = volume_down_pin_number
        self._play_pause_button = play_pause_pin_number

        self._create_buttons()

    def _create_buttons(self):
        """
        For each _xxx_button attribute, if it has been set to a pin number,
        then overwrite the attribute with a Button object that connects to that
        pin number
        """

        for button_name in BUTTON_NAMES:
            button_attr_name = "_{}_button".format(button_name)
            pin_number = getattr(self, button_attr_name)
            if pin_number is not None:
                button = Button(_BUTTON_TO_BCM_LOOKUP[pin_number])
                button.when_pressed = self._led_feedback_wrapper(
                    getattr(self, "_{}".format(button_name))
                )
                setattr(self, button_attr_name, button)

        # To mute, the "volume down" button is held
        if self._volume_down_button:
            self._volume_down_button.when_held = self._mute

    @staticmethod
    def _led_feedback_wrapper(function):
        def wrapper():
            onboard_leds.on("act")
            onboard_leds.off("act")
            function()

        return wrapper

    @staticmethod
    def _next():
        mopidy_core.next()

    @staticmethod
    def _previous():
        mopidy_core.previous()

    @staticmethod
    def _volume_up():
        sound.volume_up()

    @staticmethod
    def _volume_down():
        sound.volume_down()

    @staticmethod
    def _play_pause():
        mopidy_core.play_pause()

    @staticmethod
    def _mute():
        sound.mute()
