import logging
import pykka
from mopidy import core as mopidy_core

from .globals import (
    set_global,
    logger,
    rfid,
    buttons,
    spotify_playlist,
    onboard_leds,
    sound,
    db as db_global,
    mopidy_core as mopidy_core_global,
)
from .interface.buttons import Buttons
from .interface.mopidy_core import MopidyCore
from .interface.db import db
from .interface.onboard_leds import OnBoardLEDs
from .interface.rfid import RFID
from .interface.sound import Sound
from .interface.spotify_playlist import SpotifyPlaylist


class ChoosMoosFrontend(pykka.ThreadingActor, mopidy_core.CoreListener):
    def __init__(self, config, core):
        super(ChoosMoosFrontend, self).__init__()
        self._set_globals(config, core)

    @staticmethod
    def _set_globals(config, core):

        # logger
        set_global(logger, logging.getLogger(__name__))

        # database
        set_global(db_global, db)

        # mopidy core
        set_global(mopidy_core_global, MopidyCore(core))

        # buttons
        set_global(
            buttons,
            Buttons(
                **{
                    key: value
                    for key, value in config["choosmoos"].items()
                    if key.endswith("pin_number")
                }
            ),
        )

        # rfid
        set_global(rfid, RFID(config["choosmoos"]["nfc_demo_app_location"]))

        # spotify playlist
        set_global(
            spotify_playlist,
            SpotifyPlaylist(
                client_id=config["spotify"]["client_id"],
                client_secret=config["spotify"]["client_secret"],
            ),
        )

        # on-board LEDs
        set_global(onboard_leds, OnBoardLEDs())

        # sound
        set_global(sound, Sound())

    def on_start(self):
        logger.info("Starting ChoosMoos")
        rfid.start_reading()
        db.init()
        # we set Mopidy's Core volume to max because we will be using alsaaudio
        # to do volume control via the ALSA interface. It's possible that
        # Mopidy does this every time it starts up, but added in here for
        # completeness
        mopidy_core_global.volume_to_max()

    def on_stop(self):
        logger.info("Stopping ChoosMoos")
        rfid.stop_reading()
        db.close()
        onboard_leds.deactivate()
        sound.reset_volume()
