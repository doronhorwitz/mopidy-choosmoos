import logging
import pykka
import traceback

from mopidy import core
from .gpio_input_manager import GPIOManager


logger = logging.getLogger(__name__)


class ChoosMoosFrontend(pykka.ThreadingActor, core.CoreListener):

    def __init__(self, config, core):
        super(ChoosMoosFrontend, self).__init__()
        self.core = core
        kwargs = {key: value for key, value in config['choosmoos'].iteritems() if key.endswith('pin_number')}
        self.gpio_manager = GPIOManager(self, **kwargs)

    def playback_state_changed(self, old_state, new_state):
        self.gpio_manager.set_led(new_state == core.PlaybackState.PLAYING)

    def input(self, input_event):
        try:
            self.manage_input(input_event)
        except Exception:
            traceback.print_exc()

    def manage_input(self, input_event):
        if input_event == 'volume_up':
            self.core.playback.volume = self.core.playback.volume.get() + 10
        elif input_event == 'volume_down':
            self.core.playback.volume = self.core.playback.volume.get() - 10
        elif input_event == 'mute':
            self.core.playback.volume = 0
        elif input_event == 'next':
            self.core.playback.next()
        elif input_event == 'previous':
            self.core.playback.previous()
        elif input_event['key'] == 'play_pause':
            if self.core.playback.state.get() == core.PlaybackState.PLAYING:
                self.core.playback.pause()
            else:
                self.core.playback.play()
