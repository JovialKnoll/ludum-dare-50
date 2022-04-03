import pygame

import constants
import mode


class ModeFly0(mode.ModeFly):
    __slots__ = (
    )

    def __init__(self):
        super().__init__()
        pygame.mixer.music.load(constants.MUSIC0)
        pygame.mixer.music.play(-1)

    def _getSpawnWait(self):
        return 3000

    def _getKillAmount(self):
        return 4

    def _getEnemyLevel(self):
        if self._kill_count_down < self._getKillAmount():
            return 2
        return 1

    def _success(self):
        self.next_mode = mode.ModePre1()
