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
        self.gpio_manager = GPIOManager(self, config['ttsgpio'])

    def track_playback_started(self, tl_track):
        pass

    def playback_state_changed(self, old_state, new_state):
        self.gpio_manager.set_led(new_state == core.PlaybackState.PLAYING)

    def input(self, input_event):
        try:
            self.manage_input(input_event)
        except Exception:
            traceback.print_exc()

    def manage_input(self, input_event):
        if input_event['key'] == 'volume_up':
            current = self.core.playback.volume.get()
            current += 10
            self.core.playback.volume = current
        elif input_event['key'] == 'volume_down':
            if input_event['long']:
                current = 0
            else:
                current = self.core.playback.volume.get()
                current -= 10
            self.core.playback.volume = current
        elif input_event['key'] == 'next':
            self.core.playback.next()
        elif input_event['key'] == 'previous':
            self.core.playback.previous()
        elif input_event['key'] == 'main':
            if self.core.playback.state.get() == core.PlaybackState.PLAYING:
                self.core.playback.pause()
            else:
                self.core.playback.play()

    def playlists_loaded(self):
        self.main_menu.elements[0].reload_playlists()
        self.tts.speak_text("Playlists loaded")
