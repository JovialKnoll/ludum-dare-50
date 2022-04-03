import pygame
import jovialengine

import constants
import mode


class ModeOpening6(mode.ModeOpening):
    __slots__ = (
    )

    def __init__(self):
        super().__init__()
        self._background.fill(constants.BLACK)
        jovialengine.shared.font_wrap.renderToInside(
            self._background,
            (constants.SCREEN_SIZE[0] // 8, constants.SCREEN_SIZE[1] // 8),
            constants.SCREEN_SIZE[0] // 2 + constants.SCREEN_SIZE[0] // 4,
            "* Make sure not to FIRE until you have enough energy to THREATEN the SPACE BEASTS!"
            + " You must hit at least one."
            + "\n\n* The SPACE BEASTS are COLOR CODED for how much energy they'll require!"
            + "\n\nGood Luck!",
            constants.WHITE,
            constants.BLACK
        )
        text = "press any key to proceed"
        text_width = jovialengine.shared.font_wrap.font.size(text)[0]
        jovialengine.shared.font_wrap.renderTo(
            self._background,
            (constants.SCREEN_SIZE[0] - text_width - 4, constants.SCREEN_SIZE[1] - constants.FONT_HEIGHT),
            text,
            constants.WHITE,
            constants.BLACK
        )
        ship_image = pygame.image.load(constants.SHIP).convert()
        ship_image.set_colorkey(constants.COLORKEY)
        ship_rect = ship_image.get_rect()
        ship_rect.midbottom = (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] - ship_rect.height)
        pygame.Surface.blit(
            self._background,
            ship_image,
            ship_rect
        )

    def _switchMode(self):
        self.next_mode = mode.ModeFly0()
