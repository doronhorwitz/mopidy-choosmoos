import logging
import pykka
import traceback

from mopidy import core
from .gpio_input_manager import GPIOManager


logger = logging.getLogger(__name__)


DEFAULT_NFC_DEMO_APP_LOCATION = '/home/pi/pn7150/linux_libnfc-nci'


class ChoosMoosFrontend(pykka.ThreadingActor, core.CoreListener):

    def __init__(self, config, core):
        super(ChoosMoosFrontend, self).__init__()
        self._core = core
        config = config['choosmoos']
        pin_number_kwargs = {key: value for key, value in config.iteritems() if key.endswith('pin_number')}
        self.gpio_manager = GPIOManager(
            self,
            nfc_demo_app_location=config['nfc_demo_app_location'] or DEFAULT_NFC_DEMO_APP_LOCATION,
            **pin_number_kwargs
        )

    def on_stop(self):
        logger.info('Stopping ChoosMoos')
        self.gpio_manager.stop()

    def input(self, input_event):
        try:
            self.manage_input(input_event)
        except Exception:
            traceback.print_exc()

    def manage_input(self, input_event):
        if input_event == 'volume_up':
            self._core.playback.volume = self._core.playback.volume.get() + 10
        elif input_event == 'volume_down':
            self._core.playback.volume = self._core.playback.volume.get() - 10
        elif input_event == 'mute':
            self._core.playback.volume = 0
        elif input_event == 'next':
            self._core.playback.next()
        elif input_event == 'previous':
            self._core.playback.previous()
        elif input_event == 'play_pause':
            if self._core.playback.state.get() == core.PlaybackState.PLAYING:
                self._core.playback.pause()
            else:
                self._core.playback.play()
