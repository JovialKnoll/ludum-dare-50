from .modefly import ModeFly


class ModeFly0(ModeFly):
    __slots__ = (
    )

    def __init__(self):
        super().__init__()

    def _getSpawnWait(self):
        return 3000

    def _getKillAmount(self):
        return 4

    def _getEnemyLevel(self):
        if self._kill_count_down < self._getKillAmount():
            return 2
        return 1
