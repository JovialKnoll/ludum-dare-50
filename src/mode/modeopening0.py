import pygame
import jovialengine

import constants
from .modeopening import ModeOpening
from .modeopening1 import ModeOpening1


class ModeOpening0(ModeOpening):
    _LOGO_TEXT = "JovialKnoll"

    __slots__ = (
        '_time',
    )

    def __init__(self):
        super().__init__()
        self._time = 0
        self._background.fill(constants.WHITE)
        jovialengine.shared.font_wrap.renderToCentered(
            self._background,
            (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] * 5 // 8),
            self._LOGO_TEXT,
            False,
            constants.BLACK
        )
        logo = pygame.image.load(constants.JK_LOGO_BLACK).convert()
        self._background.blit(
            logo,
            (
                constants.SCREEN_SIZE[0] // 2 - logo.get_width() // 2,
                constants.SCREEN_SIZE[1] * 7 // 16 - logo.get_height() // 2,
            )
        )

    def _switchMode(self):
        self.next_mode = ModeOpening1()

    def _update(self, dt):
        self._time += dt
        if self._time >= 1500:
            self._stopMixer()
            self._switchMode()
