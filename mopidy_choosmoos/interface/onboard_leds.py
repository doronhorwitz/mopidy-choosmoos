from mopidy_choosmoos.utils.onboard_leds import ActOnBoardLED, PwrOnBoardLED


class OnBoardLEDs:
    def __init__(self):
        self._onboard_leds = {
            "act": ActOnBoardLED(),
            "pwr": PwrOnBoardLED(),
        }

    def deactivate(self):
        for onboard_led in self._onboard_leds.values():
            onboard_led.deactivate()

    def on(self, led_name):
        self._onboard_leds[led_name].on()

    def off(self, led_name):
        self._onboard_leds[led_name].off()

    def flash(self, led_name):
        self._onboard_leds[led_name].flash()
