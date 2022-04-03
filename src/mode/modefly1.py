import random

import mode


class ModeFly1(mode.ModeFly):
    __slots__ = (
    )

    def __init__(self):
        super().__init__()

    def _getSpawnWait(self):
        return 2500

    def _getKillAmount(self):
        return 16

    def _getEnemyLevel(self):
        level = 1
        if self._kill_count_down <= 4:
            level = 4
        elif self._kill_count_down <= 8:
            level = 3
        elif self._kill_count_down <= 12:
            level = 2
        if random.random() < 0.15:
            level = min(4, level + 1)
        return level
