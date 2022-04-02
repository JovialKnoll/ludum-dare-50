import abc

import pygame
import jovialengine

import constants


class ModeFly(jovialengine.ModeBase, abc.ABC):
    SPACE_WIDTH = 672
    SPACE_HEIGHT = 360
    SPACE_SIZE = (SPACE_WIDTH, SPACE_HEIGHT)
    SPACE_BORDER = 16
    BAR_WIDTH = 632
    BAR_HEIGHT = 24
    BAR_BORDER_HEIGHT = 32
    BAR_OFFSET = (BAR_BORDER_HEIGHT - BAR_HEIGHT) // 2
    BAR_BORDER_COLOR = (105, 105, 124)
    BAR_CHARGE_SPEED = 0.001 / 8
    __slots__ = (
        '_charge',
    )

    def __init__(self):
        self._init(self.SPACE_SIZE)
        self._camera.move_ip(self.SPACE_BORDER, self.SPACE_BORDER)
        self._background.fill(constants.BLACK)
        self._charge = 0.0

    def _input(self, event: pygame.event.Event):
        # player movement, controls, etc
        pass

    def _update(self, dt: int):
        self._charge += dt * self.BAR_CHARGE_SPEED
        if self._charge > 1.0:
            self._charge = 1.0
        pass

    def _updatePreDraw(self, screen: pygame.surface.Surface):
        pass

    def _drawPreSprites(self, screen: pygame.surface.Surface):
        pass

    def _drawPostSprites(self, screen: pygame.surface.Surface):
        pass

    def _drawPostCamera(self, screen: pygame.surface.Surface):
        # bar border
        screen.fill(
            self.BAR_BORDER_COLOR,
            (
                0,
                constants.SCREEN_SIZE[1] - self.BAR_BORDER_HEIGHT,
                constants.SCREEN_SIZE[0],
                self.BAR_BORDER_HEIGHT
            )
        )
        # unfilled bar
        screen.fill(
            constants.BLACK,
            (
                self.BAR_OFFSET,
                constants.SCREEN_SIZE[1] - self.BAR_BORDER_HEIGHT + self.BAR_OFFSET,
                self.BAR_WIDTH,
                self.BAR_HEIGHT
            )
        )
        # filled bar

        bar_color_component = int(self._charge * 255)
        bar_color = (bar_color_component, 0, 255 - bar_color_component)
        screen.fill(
            bar_color,
            (
                self.BAR_OFFSET,
                constants.SCREEN_SIZE[1] - self.BAR_BORDER_HEIGHT + self.BAR_OFFSET,
                self.BAR_WIDTH * self._charge,
                self.BAR_HEIGHT
            )
        )
