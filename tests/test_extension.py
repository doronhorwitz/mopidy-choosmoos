from __future__ import unicode_literals

from mopidy_choosmoos import Extension


def test_get_default_config():
    ext = Extension()

    config = ext.get_default_config()

    assert "[choosmoos]" in config
    assert "nfc_demo_app_location =" in config
    assert "next_pin_number = 3" in config
    assert "previous_pin_number = 4" in config
    assert "volume_up_pin_number = 1" in config
    assert "volume_down_pin_number = 2" in config
    assert "play_pause_pin_number = 5" in config


def test_get_config_schema():
    ext = Extension()

    schema = ext.get_config_schema()

    assert "next_pin_number" in schema
    assert "previous_pin_number" in schema
    assert "volume_up_pin_number" in schema
    assert "volume_down_pin_number" in schema
    assert "play_pause_pin_number" in schema
    assert "nfc_demo_app_location" in schema
