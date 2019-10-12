import logging
import pykka
from mopidy import core as mopidy_core

from .globals import set_global, rfid, core as core_global, buttons, spotify_playlist, db as db_global
from .interface.buttons import Buttons
from .interface.core import Core
from .interface.db import db
from .interface.rfid import RFID
from .interface.spotify_playlist import SpotifyPlaylist


logger = logging.getLogger(__name__)


class ChoosMoosFrontend(pykka.ThreadingActor, mopidy_core.CoreListener):

    def __init__(self, config, core):
        super(ChoosMoosFrontend, self).__init__()
        self._set_globals(config, core)

    @staticmethod
    def _set_globals(config, core):

        # database
        set_global(db_global, db)

        # mopidy core
        set_global(core_global, Core(core))

        # buttons
        set_global(buttons, Buttons(**{key: value for key, value in config['choosmoos'].iteritems()
                                       if key.endswith('pin_number')}))

        # rfid
        set_global(rfid, RFID(config['choosmoos']['nfc_demo_app_location']))

        # spotify playlist
        set_global(spotify_playlist, SpotifyPlaylist(
            client_id=config['spotify']['client_id'],
            client_secret=config['spotify']['client_secret']
        ))

    def on_start(self):
        logger.info('Starting ChoosMoos')
        rfid.start_reading()
        db.init()

    def on_stop(self):
        logger.info('Stopping ChoosMoos')
        rfid.stop_reading()
        db.close()
