from mopidy import core
from operator import add, sub
from .db import Playlist
from ..globals import spotify_playlist, onboard_leds


class MopidyCore:
    def __init__(self, core_):
        self._core = core_
        self._volume_before_muted = None
        self._current_track_number = None
        self._number_of_tracks = None
        self._current_track_length = None

    def volume_to_max(self):
        self._core.playback.volume = 100

    def _change_track(self, operation, core_function):
        new_track_number = operation(self._current_track_number, 1)
        if 1 <= new_track_number <= self._number_of_tracks:
            self._current_track_number = new_track_number
            self._current_track_length = (
                self._core.playback.get_current_track().get().length
            )
            core_function()

    def next(self):
        self._change_track(add, self._core.playback.next)

    def previous(self):
        self._change_track(sub, self._core.playback.previous)

    def _set_time_position(self, operation):
        current_time_position = self._core.playback.get_time_position().get()
        new_time_position = operation(current_time_position, 5000)
        if 0 < new_time_position < self._current_track_length:
            self._core.playback.seek(new_time_position)

    def seek_forward(self):
        self._set_time_position(add)

    def seek_backward(self):
        self._set_time_position(sub)

    def play_pause(self):
        if self._core.playback.get_state().get() == core.PlaybackState.PLAYING:
            self._core.playback.pause()
        else:
            self._core.playback.play()

    def load_playlist(self, tag_uuid):
        playlist = Playlist.select().where(Playlist.tag_uuid == tag_uuid).first()

        if not playlist:
            return

        onboard_leds.flash("act")

        # clear the playlist
        self._core.tracklist.clear()

        # get the list of tracks in the playlist
        track_uris = spotify_playlist.get_tracks(playlist.playlist_uri)

        # if there are any tracks
        if track_uris:
            # add just the first track - mopidy seems to handle better if you
            # just load one track into the playlist and play it. And only
            # afterwards load the remainder of the tracks
            self._core.tracklist.add(uris=[track_uris[0]])
            # start playing
            self._core.playback.play()
            # load the remainder of the tracks
            self._core.tracklist.add(uris=track_uris[1:])

            self._number_of_tracks = len(track_uris)
            self._current_track_number = 1
