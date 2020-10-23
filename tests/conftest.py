import pytest
import os
from gpiozero import Device
from gpiozero.pins.mock import MockFactory
from mopidy import core as mopidy_core
from mopidy_choosmoos import frontend as frontend_lib
from tests import dummy_mixer, dummy_audio, dummy_backend


def mock_system(val):
    pass


@pytest.fixture
def frontend(monkeypatch):
    config = {
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

    monkeypatch.setattr(os, "system", mock_system)
    Device.pin_factory = MockFactory()
    mixer = dummy_mixer.create_proxy()
    audio = dummy_audio.create_proxy()
    backend = dummy_backend.create_proxy(audio=audio)
    core = mopidy_core.Core.start(audio=audio, mixer=mixer, backends=[backend]).proxy()
    return frontend_lib.ChoosMoosFrontend(config, core)
