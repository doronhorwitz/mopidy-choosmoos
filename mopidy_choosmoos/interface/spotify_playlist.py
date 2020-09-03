import requests
import time
from operator import itemgetter


_TOKEN_URL = "https://auth.mopidy.com/spotify/token"
_PLAYLIST_URL = "https://api.spotify.com/v1/playlists/{playlist_uri}"
_ALL_PLAYLISTS_URL = "https://api.spotify.com/v1/me/playlists"


class SpotifyPlaylist:
    def __init__(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret
        self._access_token = None
        self._access_token_expires_at = None

    def _get_spotify_token(self):
        if (
            not self._access_token
            or not self._access_token_expires_at
            or time.time() > self._access_token_expires_at
        ):
            self._access_token, expires_in = itemgetter("access_token", "expires_in")(
                requests.post(
                    _TOKEN_URL,
                    data={
                        "client_id": self._client_id,
                        "client_secret": self._client_secret,
                        "grant_type": "client_credentials",
                    },
                ).json()
            )

            self._access_token_expires_at = time.time() + expires_in

        return self._access_token

    def _make_request(self, url, **kwargs):
        return requests.get(
            url.format(**kwargs),
            headers={
                "Authorization": "Bearer {access_token}".format(
                    access_token=self._get_spotify_token()
                )
            },
        ).json()

    def get_tracks(self, playlist_uri):
        playlist_uri = playlist_uri.split(":")[-1]
        response = self._make_request(_PLAYLIST_URL, playlist_uri=playlist_uri)
        return [track["track"]["uri"] for track in response["tracks"]["items"]]

    def get_all_playlists(self):
        response = self._make_request(_ALL_PLAYLISTS_URL)
        return [dict(uri=item["id"], name=item["name"]) for item in response["items"]]
