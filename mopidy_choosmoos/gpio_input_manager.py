import logging
from gpiozero import Button, LED
from .pn7150 import PN7150

logger = logging.getLogger(__name__)


class GPIOManager(object):

    def __init__(self, frontend, led_pin_number=None, next_pin_number=None, previous_pin_number=None,
                 volume_up_pin_number=None, volume_down_pin_number=None, play_pause_pin_number=None):
        self._frontend = frontend
        self._led = LED(led_pin_number) if led_pin_number else None

        if next_pin_number:
            Button(next_pin_number).when_pressed = self._next
        if previous_pin_number:
            Button(previous_pin_number).when_pressed = self._previous
        if volume_up_pin_number:
            Button(volume_up_pin_number).when_pressed = self._volume_up
        if volume_down_pin_number:
            Button(volume_down_pin_number).when_pressed = self._volume_down
            Button(volume_down_pin_number).when_held = self._mute
        if play_pause_pin_number:
            Button(play_pause_pin_number).when_pressed = self._play_pause

        pn7150 = PN7150('/home/pi/pn7150/linux_libnfc-nci')
        pn7150.when_tag_read = self._play_pause
        pn7150.start_reading()

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

    def set_led(self, on):
        if self._led:
            if on:
                self._led.on()
            else:
                self._led.off()
