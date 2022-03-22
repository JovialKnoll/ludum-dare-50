import pygame
import jovialengine

import constants
from .modeopening import ModeOpening


class ModeOpening1(ModeOpening):
    __slots__ = (
    )

    def __init__(self):
        super().__init__()
        self._background.fill(constants.WHITE)
        jovialengine.shared.font_wrap.renderToCentered(
            self._background,
            (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] // 2 + constants.FONT_SIZE // 2),
            "press any key to start",
            constants.BLACK,
            constants.WHITE
        )
        title_font = pygame.font.Font(constants.TITLE_FONT, int(constants.FONT_SIZE * 1.5))
        title_font_wrap = jovialengine.FontWrap(title_font, int(constants.FONT_HEIGHT * 1.5), False)
        title_font_wrap.renderToCentered(
            self._background,
            (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] // 4),
            constants.TITLE,
            constants.BLACK,
            constants.WHITE
        )
        version_width = jovialengine.shared.font_wrap.font.size(constants.VERSION)[0]
        jovialengine.shared.font_wrap.renderTo(
            self._background,
            (constants.SCREEN_SIZE[0] - version_width - 4, constants.SCREEN_SIZE[1] - constants.FONT_HEIGHT),
            constants.VERSION,
            constants.BLACK,
            constants.WHITE
        )

    def _switchMode(self):
        self.next_mode = None
