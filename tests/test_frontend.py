import pykka
import os
from mopidy_choosmoos import Extension
from mopidy_choosmoos import frontend as frontend_lib
from mopidy_choosmoos.web import choosmoos_web_factory
from unittest import mock
from unittest.mock import call


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


def test_anything(frontend):

    frontend.on_start()

    stop_mopidy_core()
