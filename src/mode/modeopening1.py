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
            constants.BLACK
        )
        title_font = pygame.font.Font(constants.TITLE_FONT, int(constants.FONT_SIZE * 1.5))
        title_font_wrap = jovialengine.FontWrap(title_font, False)
        title_font_wrap.renderToCentered(
            self._background,
            (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] // 4),
            constants.TITLE,
            constants.BLACK
        )
        version_width = len(constants.VERSION) * constants.FONT_SIZE
        jovialengine.shared.font_wrap.renderToInside(
            self._background,
            (constants.SCREEN_SIZE[0] - version_width, constants.SCREEN_SIZE[1] - constants.FONT_HEIGHT),
            version_width,
            constants.VERSION,
            constants.BLACK
        )

    def _switchMode(self):
        self.next_mode = None
