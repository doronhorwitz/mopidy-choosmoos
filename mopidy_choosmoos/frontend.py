import logging
import pykka
from mopidy import core as mopidy_core

from .buttons import Buttons
from .db import db
from .globals import set_global, rfid, db, core as core_global, buttons, spotify_playlist, db as db_global
from .rfid import RFID
from .spotify_playlist import SpotifyPlaylist


logger = logging.getLogger(__name__)


DEFAULT_NFC_DEMO_APP_LOCATION = '/home/pi/pn7150/linux_libnfc-nci'


class ChoosMoosFrontend(pykka.ThreadingActor, mopidy_core.CoreListener):

    def __init__(self, config, core):
        super(ChoosMoosFrontend, self).__init__()
        self._set_globals(config, core)

    @staticmethod
    def _set_globals(config, core):

        set_global(db_global, db)
        db.init()

        # mopidy core
        set_global(core_global, core)

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

    def on_stop(self):
        logger.info('Stopping ChoosMoos')
        rfid.stop_reading()
        db.close()
