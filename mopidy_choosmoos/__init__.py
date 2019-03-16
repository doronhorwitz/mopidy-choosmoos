from __future__ import unicode_literals

import logging
import os

from mopidy import config, ext

import mem

from .frontend import ChoosMoosFrontend
from .message_bus import MessageBus
from .web import choosmoos_web_factory



__version__ = '0.1.0'

logger = logging.getLogger(__name__)



class Extension(ext.Extension):

    dist_name = 'Mopidy-ChoosMoos'
    ext_name = 'choosmoos'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        for pin_name in ['next', 'previous', 'volume_up', 'volume_down', 'play_pause']:
            schema['{}_pin_number'.format(pin_name)] = config.Integer(optional=True)
        schema['nfc_demo_app_location'] = config.String(optional=True)
        return schema

    def setup(self, registry):
        mem.message_bus = MessageBus()

        registry.add('frontend', ChoosMoosFrontend)

        registry.add('http:app', {
            'name': self.ext_name,
            'factory': choosmoos_web_factory,
        })
