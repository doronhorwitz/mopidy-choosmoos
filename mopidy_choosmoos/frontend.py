import logging
import pykka
import traceback

from mopidy import core

import mem

from .gpio_input_manager import GPIOManager
from .db import init as init_db, stop as stop_db, Playlist
from .spotify_playlist import SpotifyPlaylist


logger = logging.getLogger(__name__)


DEFAULT_NFC_DEMO_APP_LOCATION = '/home/pi/pn7150/linux_libnfc-nci'


class ChoosMoosFrontend(pykka.ThreadingActor, core.CoreListener):

    def __init__(self, config, core):
        super(ChoosMoosFrontend, self).__init__()
        self._core = core
        pin_number_kwargs = {key: value for key, value in config['choosmoos'].iteritems()
                             if key.endswith('pin_number')}
        self._gpio_manager = GPIOManager(
            self,
            nfc_demo_app_location=config['choosmoos']['nfc_demo_app_location'] or DEFAULT_NFC_DEMO_APP_LOCATION,
            **pin_number_kwargs
        )
        self._spotify_playlist = SpotifyPlaylist(
            client_id=config['spotify']['client_id'],
            client_secret=config['spotify']['client_secret']
        )
        init_db()
        mem.message_bus.set_spotify_playlist(self._spotify_playlist)
        mem.message_bus.set_db_playlist(Playlist)

    def on_start(self):
        logger.info('Starting ChoosMoos')

    def on_stop(self):
        logger.info('Stopping ChoosMoos')
        self._gpio_manager.stop()
        stop_db()

    def input(self, input_event, **kwargs):
        try:
            self.manage_input(input_event, **kwargs)
        except Exception:
            traceback.print_exc()

    def manage_input(self, input_event, **kwargs):
        if input_event == 'volume_up':
            self._core.playback.volume = self._core.playback.volume.get() + 5
        elif input_event == 'volume_down':
            self._core.playback.volume = self._core.playback.volume.get() - 5
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
        elif input_event == 'load_playlist':
            playlist = Playlist.select().where(Playlist.id == kwargs['playlist_id']).first()
            if playlist:
                # clear the playlist
                self._core.tracklist.clear()

                # get the list of tracks in the playlist
                track_uris = self._spotify_playlist.get_tracks(playlist.uri)

                # if there are any tracks
                if track_uris:
                    # add just the first track - mopidy seems to handle better if you just load one track into the
                    # playlist and play it. And only afterwards load the remainder of the trackers
                    self._core.tracklist.add(uri=track_uris[0])
                    # start playing
                    self._core.playback.play()

                # load the remainder of the tracks
                for track_uri in track_uris[1:]:
                    self._core.tracklist.add(uri=track_uri)
