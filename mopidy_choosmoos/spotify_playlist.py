import requests
import time
from operator import itemgetter


_TOKEN_URL = 'https://auth.mopidy.com/spotify/token'
_PLAYLIST_URL = 'https://api.spotify.com/v1/playlists/{playlist_id}'


class SpotifyPlaylist(object):

    def __init__(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret
        self._access_token = None
        self._access_token_expires_at = None

    def _get_spotify_token(self):
        if not self._access_token or not self._access_token_expires_at or time.time() > self._access_token_expires_at:
            self._access_token, expires_in = itemgetter('access_token', 'expires_in')(
                requests.post(_TOKEN_URL, data={
                    'client_id': self._client_id,
                    'client_secret': self._client_secret,
                    'grant_type': 'client_credentials',
                }).json())

            self._access_token_expires_at = time.time() + expires_in

        return self._access_token

    def get_tracks(self, playlist_uri):
        playlist_id = playlist_uri.split(':')[-1]
        access_token = self._get_spotify_token()
        response = requests.get(_PLAYLIST_URL.format(playlist_id=playlist_id), headers={
            'Authorization': 'Bearer {access_token}'.format(access_token=access_token)
        }).json()

        return [track['track']['uri'] for track in response['tracks']['items']]
