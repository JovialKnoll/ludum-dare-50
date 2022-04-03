import random

import mode


class ModeFly2(mode.ModeFly):
    __slots__ = (
    )

    def __init__(self):
        super().__init__()

    def _getSpawnWait(self):
        return 2000

    def _getKillAmount(self):
        return 32

    def _getEnemyLevel(self):
        level = 1
        if self._kill_count_down <= 10:
            level = 4
        elif self._kill_count_down <= 20:
            level = 3
        elif self._kill_count_down <= 28:
            level = 2
        if random.random() < 0.25:
            level = max(1, level - 1)
        if random.random() < 0.2:
            level = min(4, level + 1)
        return level

    def _success(self):
        self.next_mode = mode.ModeWin()
