import json
import logging
import os
import tornado.web

import mem

from uuid import uuid4

from .utils import validate_uuid4

logger = logging.getLogger(__name__)


class HttpHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def initialize(self, core, config):
        self.core = core
        self.config = config

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")

    @tornado.web.asynchronous
    def get(self, slug=None):

        if slug == 'all-playlists':
            all_spotify_playlists = mem.message_bus.get_all_spotify_playlists()
            all_db_playlists = mem.message_bus.get_all_db_playlists()
            db_playlist_lookup = {db_playlist.uri.split(':')[-1]: str(db_playlist.id)
                                  for db_playlist in all_db_playlists}

            playlists = [
                dict(name=spotify_playlist["name"], id=spotify_playlist["id"],
                     db_id=db_playlist_lookup.get(spotify_playlist["id"], None))
                for spotify_playlist in all_spotify_playlists]

            self.write(json.dumps({"playlists": playlists}))

        self.finish()


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def initialize(self, core, config):
        self.core = core

    def check_origin(self, origin):
        return True

    def open(self):
        logger.debug("QueueManager WebSocket opened")

        mem.message_bus.set_websocket(self)

    def send_json_msg(self, action, params=None):
        data_to_send = {
            'action': action
        }
        if params:
            data_to_send['params'] = params
        self.write_message(tornado.escape.json_encode(data_to_send))

    def on_message(self, message):
        if not message:
            return

        logger.debug("Message received: %s", message)

        data = tornado.escape.json_decode(message)
        action = data['action']
        if action == 'open_websocket':
            self.send_json_msg('acknowledge_open_websocket')
        elif action == 'assign_tag_to_playlist':
            playlist_id = data['params']['playlist_id']
            mem.message_bus.pn7150_stop_reading()
            self.send_json_msg('tag_write_ready', {
                'playlist_id': playlist_id
            })
            existing_text = mem.message_bus.pn7150_read_once()
            uuid = None
            if validate_uuid4(existing_text):
                uuid = existing_text
            else:
                new_uuid = str(uuid4())
                write_success = mem.message_bus.pn7150_write(new_uuid)
                if write_success:
                    uuid = new_uuid
                else:
                    self.send_json_msg('tag_assign_failure', {
                        'playlist_id': playlist_id
                    })

            if uuid:
                mem.message_bus.assign_playlist_id_to_tag(playlist_id, uuid)
                self.send_json_msg('tag_assign_success', {
                    'playlist_id': playlist_id
                })
            mem.message_bus.pn7150_start_reading()

    def on_close(self):
        logger.debug("QueueManager WebSocket closed")
        mem.message_bus.unset_websocket()


def choosmoos_web_factory(config, core):
    path = os.path.join(os.path.dirname(__file__), 'static')

    return [
        (r'/ws/?', WebSocketHandler, {
            'core': core,
            'config': config
        }),
        (r'/http/([^/]*)', HttpHandler, {
            'core': core,
            'config': config
        }),
        (r'/([^.]*)', tornado.web.StaticFileHandler, {
            'path': path + '/index.html'
        }),
        (r'/(.*)', tornado.web.StaticFileHandler, {
            'path': path
        }),
    ]
