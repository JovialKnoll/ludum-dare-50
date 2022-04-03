import pygame
import jovialengine

import constants
import gameutility
import mode


class ModeOpening1(mode.ModeOpening):
    __slots__ = (
    )

    def __init__(self):
        super().__init__()
        pygame.mixer.Sound(constants.TITLE_SOUND).play()
        self._background.fill(constants.BLACK)
        jovialengine.shared.font_wrap.renderToCentered(
            self._background,
            (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] // 2 + constants.FONT_SIZE // 2),
            "press any key to start",
            constants.WHITE,
            constants.BLACK
        )
        title_font = pygame.font.Font(constants.TITLE_FONT, int(constants.FONT_SIZE * 1.5))
        title_font_wrap = jovialengine.FontWrap(title_font, int(constants.FONT_HEIGHT * 1.5), False)
        title_surf = title_font_wrap.renderInside(
            title_font.size(constants.TITLE)[0],
            constants.TITLE,
            constants.WHITE,
            constants.BLACK
        )
        for i in range(len(constants.TITLE)):
            x = title_font.size(constants.TITLE[:i])[0]
            if i in (4, 13, 14):
                x -= 1
            elif i == 11:
                x -= 2
            elif i == 5:
                x -= 3
            elif i == 15:
                x -= 5
            title_font_wrap.renderToInside(
                title_surf,
                (x, 0),
                title_font.size(constants.TITLE[i])[0],
                constants.TITLE[i],
                gameutility.getBarColor(i / len(constants.TITLE))
            )
        title_surf_rect = title_surf.get_rect()
        title_surf_rect.center = (constants.SCREEN_SIZE[0] // 2, constants.SCREEN_SIZE[1] // 4)
        pygame.Surface.blit(
            self._background,
            title_surf,
            title_surf_rect
        )
        version_width = jovialengine.shared.font_wrap.font.size(constants.VERSION)[0]
        jovialengine.shared.font_wrap.renderTo(
            self._background,
            (constants.SCREEN_SIZE[0] - version_width - 4, constants.SCREEN_SIZE[1] - constants.FONT_HEIGHT),
            constants.VERSION,
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
        self.next_mode = mode.ModeOpening2()
