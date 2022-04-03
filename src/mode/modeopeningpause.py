import abc

import mode


class ModeOpeningPause(mode.ModeOpening, abc.ABC):
    __slots__ = (
        '_time',
        '_ready',
    )

    def __init__(self):
        super().__init__()
        self._time = 0
        self._ready = False

    def _input(self, event):
        if self._ready:
            super()._input(event)

    @abc.abstractmethod
    def _whenReady(self):
        raise NotImplementedError(
            type(self).__name__ + "._whenReady(self)"
        )

    def _update(self, dt):
        self._time += dt
        if self._time >= 1000 and not self._ready:
            self._whenReady()
            self._ready = True
