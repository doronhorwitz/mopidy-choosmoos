import traceback
import types
from mopidy import core
from operator import add, sub

from .db import Playlist
from ..globals import spotify_playlist


# https://stackoverflow.com/a/3468410/506770
# Wraps all functions in a try-except claus to print the traceback if there is one.
class CoreTracebackMeta(type):
    def __new__(mcs, name, bases, attrs):
        for attr_name, attr_value in attrs.iteritems():
            if isinstance(attr_value, types.FunctionType):
                attrs[attr_name] = mcs.decorator(attr_value)

        return super(CoreTracebackMeta, mcs).__new__(mcs, name, bases, attrs)

    @classmethod
    def decorator(mcs, func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except:
                traceback.print_exc()
                result = None
            return result
        return wrapper


class Core(object):
    __metaclass__ = CoreTracebackMeta

    def __init__(self, core_):
        self._core = core_
        self._volume_before_muted = None
        self._current_track_number = None
        self._number_of_tracks = None

    def _change_volume(self, operation):
        current_volume = self._core.playback.volume.get()
        new_volume = operation(current_volume, 5)
        if new_volume > 100:
            new_volume = 100
        elif new_volume < 0:
            new_volume = 0
        if new_volume != current_volume:
            self._core.playback.volume = new_volume

    def volume_up(self):
        if self._volume_before_muted is None:
            self._change_volume(add)
        else:
            self._core.playback.volume = self._volume_before_muted
            self._volume_before_muted = None

    def volume_down(self):
        if self._volume_before_muted is None:
            self._change_volume(sub)

    def mute(self):
        self._volume_before_muted = self._core.playback.volume.get()
        self._core.playback.volume = 0

    def _change_track(self, operation, core_function):
        new_track_number = operation(self._current_track_number, 1)
        if 1 <= new_track_number <= self._number_of_tracks:
            self._current_track_number = new_track_number
            core_function()

    def next(self):
        self._change_track(add, self._core.playback.next)

    def previous(self):
        self._change_track(sub, self._core.playback.previous)

    def play_pause(self):
        if self._core.playback.state.get() == core.PlaybackState.PLAYING:
            self._core.playback.pause()
        else:
            self._core.playback.play()

    def load_playlist(self, tag_uuid):
        playlist = Playlist.select().where(Playlist.tag_uuid == tag_uuid).first()

        if not playlist:
            return

        # clear the playlist
        self._core.tracklist.clear()

        # get the list of tracks in the playlist
        track_uris = spotify_playlist.get_tracks(playlist.playlist_uri)

        # if there are any tracks
        if track_uris:
            # add just the first track - mopidy seems to handle better if you just load one track into the
            # playlist and play it. And only afterwards load the remainder of the tracks
            self._core.tracklist.add(uri=track_uris[0])
            # start playing
            self._core.playback.play()
            # load the remainder of the tracks
            for track_uri in track_uris[1:]:
                self._core.tracklist.add(uri=track_uri)

            self._number_of_tracks = len(track_uris)
            self._current_track_number = 1
