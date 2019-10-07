import traceback
import types
from mopidy import core

from .db import Playlist
from .globals import spotify_playlist


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

    def volume_up(self):
        self._core.playback.volume = self._core.playback.volume.get() + 5

    def volume_down(self):
        self._core.playback.volume = self._core.playback.volume.get() - 5

    def mute(self):
        self._core.playback.volume = 0

    def next(self):
        self._core.playback.next()

    def previous(self):
        self._core.playback.previous()

    def play_pause(self):
        if self._core.playback.state.get() == core.PlaybackState.PLAYING:
            self._core.playback.pause()
        else:
            self._core.playback.play()

    def load_playlist(self, playlist_id):
        playlist = Playlist.select().where(Playlist.id == playlist_id).first()

        if not playlist:
            return

        # clear the playlist
        self._core.tracklist.clear()

        # get the list of tracks in the playlist
        track_uris = spotify_playlist.get_tracks(playlist.uri)

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
