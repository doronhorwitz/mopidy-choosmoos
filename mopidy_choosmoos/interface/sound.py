from operator import add, sub

try:
    from alsaaudio import Mixer
except ModuleNotFoundError:
    pass

from mopidy_choosmoos.utils import floor_to_base_int


class Sound:
    _VOLUME_DELTA = 5

    def __init__(self):
        self._mixer = Mixer("PCM")
        self._volume_before_muted = None
        self._old_volumes, self._current_volume = self._init_volume()

    def _init_volume(self):
        old_volumes = self._mixer.getvolume()
        # use floor_to_base_int to round down to a multiple of _VOLUME_DELTA
        min_volume = floor_to_base_int(min(old_volumes), self._VOLUME_DELTA)
        self._mixer.setvolume(min_volume)
        return old_volumes, min_volume

    def reset_volume(self):
        for channel in range(2):
            self._mixer.setvolume(self._old_volumes[channel], channel)

    def _change_volume(self, operation=None, exact_value=None):
        if operation is not None:
            new_volume = operation(self._current_volume, self._VOLUME_DELTA)
        elif exact_value is not None:
            new_volume = exact_value
        else:
            return

        if new_volume > 100:
            new_volume = 100
        elif new_volume < 0:
            new_volume = 0
        if new_volume != self._current_volume:
            self._mixer.setvolume(new_volume)
            self._current_volume = new_volume

    def volume_up(self):
        if self._volume_before_muted is None:
            self._change_volume(add)
        else:
            self._change_volume(exact_value=self._volume_before_muted)
            self._volume_before_muted = None

    def volume_down(self):
        if self._volume_before_muted is None:
            self._change_volume(sub)

    def mute(self):
        self._volume_before_muted = self._current_volume
        self._change_volume(exact_value=0)
