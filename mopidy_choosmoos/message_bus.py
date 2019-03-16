class MessageBus(object):

    def __init__(self):
        super(MessageBus, self).__init__()
        self._websocket = None
        self._spotify_playlist = None
        self._db_playlist = None

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
