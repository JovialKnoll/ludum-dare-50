import pygame
import jovialengine

import constants
import mode


class ModeOpening2(mode.ModeOpening):
    __slots__ = (
    )

    def __init__(self):
        super().__init__()
        self._background.fill(constants.BLACK)
        jovialengine.shared.font_wrap.renderToInside(
            self._background,
            (constants.SCREEN_SIZE[0] // 8, constants.SCREEN_SIZE[1] // 8),
            constants.SCREEN_SIZE[0] // 2 + constants.SCREEN_SIZE[0] // 4,
            "You were flying a recon mission through the territory of the Space Beasts"
            + " when your ship's cooling system broke down!"
            + "\n\nOnce you start the engine again it will immediately start overheating!"
            + "\n\nBut you can't wait here any longer...",
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
        self.next_mode = mode.ModeOpening3()
