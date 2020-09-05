import os
from unittest import mock
from unittest.mock import call

import pykka
from mopidy import core

from gpiozero import Device
from gpiozero.pins.mock import MockFactory


from mopidy_choosmoos import Extension
from mopidy_choosmoos import frontend as frontend_lib

from . import dummy_audio, dummy_backend, dummy_mixer
from mopidy_choosmoos.web import choosmoos_web_factory


dummy_config = {
    "choosmoos": {
        "nfc_demo_app_location": None,
        "next_pin_number": 3,
        "previous_pin_number": 4,
        "volume_up_pin_number": 1,
        "volume_down_pin_number": 2,
        "play_pause_pin_number": 5,
    },
    "spotify": {
        "username": "alice",
        "password": "password",
        "bitrate": 160,
        "volume_normalization": True,
        "private_session": False,
        "timeout": 10,
        "allow_cache": True,
        "allow_network": True,
        "allow_playlists": True,
        "search_album_count": 20,
        "search_artist_count": 10,
        "search_track_count": 50,
        "toplist_countries": ["GB", "US"],
        "client_id": "abcd1234",
        "client_secret": "YWJjZDEyMzQ=",
    },
}


def dummy_mopidy_core():
    mixer = dummy_mixer.create_proxy()
    audio = dummy_audio.create_proxy()
    backend = dummy_backend.create_proxy(audio=audio)
    return core.Core.start(audio=audio, mixer=mixer, backends=[backend]).proxy()


def stop_mopidy_core():
    pykka.ActorRegistry.stop_all()


def test_get_frontend_classes():
    ext = Extension()
    registry = mock.Mock()

    ext.setup(registry)

    registry.add.assert_has_calls(
        [
            call("frontend", frontend_lib.ChoosMoosFrontend),
            call(
                "http:app",
                {
                    "name": "choosmoos",
                    "factory": choosmoos_web_factory,
                },
            ),
        ]
    )

    stop_mopidy_core()


def test_anything(monkeypatch):
    def mock_system(val):
        pass

    monkeypatch.setattr(os, "system", mock_system)

    Device.pin_factory = MockFactory()
    frontend_lib.ChoosMoosFrontend(dummy_config, dummy_mopidy_core())

    stop_mopidy_core()
