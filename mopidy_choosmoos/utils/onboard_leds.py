import os


class _OnBoardLED:
    # Activate:
    # $ echo none | sudo tee /sys/class/leds/led0/trigger >> /dev/null
    # $ echo gpio | sudo tee /sys/class/leds/led1/trigger >> /dev/null
    #
    # Deactivate
    # $ echo mmc0 | sudo tee /sys/class/leds/led0/trigger >> /dev/null
    # $ echo input | sudo tee /sys/class/leds/led1/trigger >> /dev/null
    #
    # Turn on
    # $ echo 1 | sudo tee /sys/class/leds/led0/brightness >> /dev/null
    # $ echo 1 | sudo tee /sys/class/leds/led1/brightness >> /dev/null
    #
    # Turn off
    # $ echo 1 | sudo tee /sys/class/leds/led0/brightness >> /dev/null
    # $ echo 1 | sudo tee /sys/class/leds/led1/brightness >> /dev/null

    # https://gpiozero.readthedocs.io/en/stable/recipes_advanced.html#controlli
    # ng-the-pi-s-own-leds
    # https://raspberrypi.stackexchange.com/questions/70013/raspberry-pi-3-mode
    # l-b-system-leds

    _LED_NUMBER = None
    _ACTIVATED_CONTENT = None
    _DEACTIVATED_CONTENT = None

    _CMD_FORMAT = (
        "echo {content} | sudo tee /sys/class/leds/led{led_number}/{type} >> /dev/null"
    )

    def __init__(self):
        self._run_command(self._ACTIVATED_CONTENT, self._LED_NUMBER, "trigger")
        self.off()

    def deactivate(self):
        self._run_command(self._DEACTIVATED_CONTENT, self._LED_NUMBER, "trigger")

    def on(self):
        self._run_command(1, self._LED_NUMBER, "brightness")

    def off(self):
        self._run_command(0, self._LED_NUMBER, "brightness")

    def flash(self):
        # the response time of the on-board LEDs is slow enough that calling
        # on() and then off() immediately after shows a nice visible blink
        self.on()
        self.off()

    @classmethod
    def _run_command(cls, content, led_number, type_):
        os.system(
            cls._CMD_FORMAT.format(content=content, led_number=led_number, type=type_)
        )


class ActOnBoardLED(_OnBoardLED):
    _LED_NUMBER = 0
    _ACTIVATED_CONTENT = "none"
    _DEACTIVATED_CONTENT = "mmc0"


class PwrOnBoardLED(_OnBoardLED):
    _LED_NUMBER = 1
    _ACTIVATED_CONTENT = "gpio"
    _DEACTIVATED_CONTENT = "input"
