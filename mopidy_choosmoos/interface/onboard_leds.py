from mopidy_choosmoos.utils.onboard_leds import ActOnBoardLED, PwrOnBoardLED


class OnBoardLEDs(object):
    def __init__(self):
        self._onboard_leds = {
            'act': ActOnBoardLED(),
            'pwr': PwrOnBoardLED(),
        }

    def deactivate(self):
        for onboard_led in self._onboard_leds.values():
            onboard_led.deactivate()

    def on(self, led_name):
        self._onboard_leds[led_name].on()

    def off(self, led_name):
        self._onboard_leds[led_name].off()

    def flash(self, led_name):
        # the response time of the on-board LEDs is slow enough that calling on() and then off() immediately after shows
        # a nice visible blink
        self.on(led_name)
        self.off(led_name)
