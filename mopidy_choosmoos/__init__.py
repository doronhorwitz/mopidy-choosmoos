from __future__ import unicode_literals

import logging
import os

from mopidy import config, ext

from .frontend import ChoosMoosFrontend
from .interface.buttons import BUTTON_NAMES
from .web import choosmoos_web_factory


__version__ = "1.0.0"

logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = "Mopidy-ChoosMoos"
    ext_name = "choosmoos"
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), "ext.conf")
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        for pin_name in BUTTON_NAMES:
            schema["{}_pin_number".format(pin_name)] = config.Integer(optional=True)
        schema["nfc_demo_app_location"] = config.String(optional=True)
        return schema

    def setup(self, registry):
        registry.add("frontend", ChoosMoosFrontend)

        registry.add(
            "http:app",
            {
                "name": self.ext_name,
                "factory": choosmoos_web_factory,
            },
        )
