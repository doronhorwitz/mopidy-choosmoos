class MessageBus(object):

    def __init__(self):
        super(MessageBus, self).__init__()
        self._websocket = None
        self._spotify_playlist = None
        self._db_playlist = None
        self._pn7150 = None

    def set_websocket(self, websocket):
        self._websocket = websocket

    def unset_websocket(self):
        self._websocket = None

    def send_websocket_message(self, msg):
        if self._websocket:
            self._websocket.write_message(msg)

    def set_spotify_playlist(self, spotify_playlist):
        self._spotify_playlist = spotify_playlist

    def get_all_spotify_playlists(self):
        if self._spotify_playlist:
            return self._spotify_playlist.get_all_playlists()

    def set_db_playlist(self, db_playlist):
        self._db_playlist = db_playlist

    def get_all_db_playlists(self):
        if self._db_playlist:
            return list(self._db_playlist.select())

    def assign_playlist_id_to_tag(self, playlist_id, tag_uuid):
        self._db_playlist.replace(id=tag_uuid, uri=playlist_id).execute()

    def set_pn7150(self, pn7150):
        self._pn7150 = pn7150

    def pn7150_write(self, text):
        return self._pn7150.write(text)

    def pn7150_read_once(self):
        return self._pn7150.read_once()

    def pn7150_stop_reading(self):
        self._pn7150.stop_reading()

    def pn7150_start_reading(self):
        self._pn7150.start_reading()
