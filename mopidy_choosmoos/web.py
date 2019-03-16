import json
import logging
import os
import tornado.web

import mem

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

    def on_message(self, message):
        if not message:
            return

        logger.debug("Message received: %s", message)

        self.write_message('hi back!')

        # data = tornado.escape.json_decode(message)
        #
        # if type(data['data']) is dict:
        #     args = data['data']
        # else:
        #     args = {}
        #
        # call = getattr(mem.queuemanager, data['method'])(**args)
        #
        # result = {
        #     'call': call,
        #     'id': data['id']
        # }
        #
        # self.write_message(json.dumps(result))

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
