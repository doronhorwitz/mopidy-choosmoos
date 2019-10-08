import json
import logging
import os
import tornado.escape
import tornado.web
import tornado.websocket
from uuid import uuid4

from .globals import set_global, reset_global, rfid, db, spotify_playlist, websocket
from .utils import validate_uuid4


logger = logging.getLogger(__name__)


class HttpHandler(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def set_default_headers(self):
        self.set_header("Content-Type", "application/json")

    @tornado.web.asynchronous
    def get(self, slug=None):

        if slug == 'all-playlists':
            all_spotify_playlists = spotify_playlist.get_all_playlists()
            all_db_playlists = db.get_all_playlists()
            db_playlist_lookup = {db_playlist.playlist_uri.split(':')[-1]: str(db_playlist.tag_uuid)
                                  for db_playlist in all_db_playlists}

            playlists = [
                dict(name=spotify_playlist_["name"],
                     playlist_uri=spotify_playlist_["uri"],
                     tag_uuid=db_playlist_lookup.get(spotify_playlist_["uri"], None))
                for spotify_playlist_ in all_spotify_playlists]

            self.write(json.dumps({"playlists": playlists}))

        self.finish()


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def data_received(self, chunk):
        pass

    def check_origin(self, origin):
        return True

    def open(self):
        logger.debug("QueueManager WebSocket opened")
        set_global(websocket, self)

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
            playlist_uri = data['params']['playlist_uri']
            rfid.stop_reading()
            self.send_json_msg('tag_write_ready', {
                'playlist_uri': playlist_uri
            })
            existing_text = rfid.read_once(wait_for_tag_removal=False)
            tag_uuid = None
            if validate_uuid4(existing_text):
                tag_uuid = existing_text
            else:
                new_uuid = str(uuid4())
                write_success = rfid.write(new_uuid, wait_for_tag_removal=False)
                if write_success:
                    tag_uuid = new_uuid
                else:
                    self.send_json_msg('tag_assign_failure', {
                        'playlist_uri': playlist_uri
                    })
            if tag_uuid:
                db.assign_playlist_uri_to_tag_uuid(tag_uuid, playlist_uri)
                self.send_json_msg('tag_assign_success', {
                    'playlist_uri': playlist_uri,
                    'tag_uuid': tag_uuid,
                })
            rfid.start_reading()

    def on_close(self):
        logger.debug("QueueManager WebSocket closed")
        reset_global(websocket)


def choosmoos_web_factory(config, core):
    path = os.path.join(os.path.dirname(__file__), 'static')

    return [
        (r'/ws/?', WebSocketHandler, {}),
        (r'/http/([^/]*)', HttpHandler, {}),
        (r'/([^.]*)', tornado.web.StaticFileHandler, {
            'path': path + '/index.html'
        }),
        (r'/(.*)', tornado.web.StaticFileHandler, {
            'path': path
        }),
    ]
