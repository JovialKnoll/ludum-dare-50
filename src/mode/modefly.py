import abc
import random

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
    STAR_DELAY = 25
    BACKGROUND_TIME = 2000
    __slots__ = (
        '_background_sprites',
        '_star_timer',
        '_star_image_0',
        '_charge',
    )

    def __init__(self):
        self._init(self.SPACE_SIZE)
        self._camera = pygame.rect.Rect(
            self.SPACE_BORDER,
            self.SPACE_BORDER,
            self.SPACE_WIDTH - (self.SPACE_BORDER * 2),
            self.SPACE_HEIGHT - (self.SPACE_BORDER * 2)
        )
        self._camera.move_ip(self.SPACE_BORDER, self.SPACE_BORDER)
        self._background.fill(constants.BLACK)
        self._background_sprites = pygame.sprite.Group()
        self._star_timer = self.STAR_DELAY
        self._star_image_0 = pygame.surface.Surface((3, 3)).convert()
        self._star_image_0.fill(constants.BLACK)
        self._star_image_0.fill(constants.WHITE, (0, 1, 3, 1))
        self._star_image_0.fill(constants.WHITE, (1, 0, 1, 3))

        stars = self.BACKGROUND_TIME // self.STAR_DELAY
        for s in range(stars):
            self._makeStar(
                int(self.SPACE_WIDTH * s / stars)
            )

        self._charge = 0.0

    def _input(self, event: pygame.event.Event):
        # player movement, controls, etc
        pass

    def _makeStar(self, x):
        star_sprite = jovialengine.AnimSprite()
        star_sprite.image = self._star_image_0
        star_sprite.rect = star_sprite.image.get_rect()
        star_sprite.rect.center = (
            x + random.randint(0, self.SPACE_BORDER),
            random.randint(0, self.SPACE_HEIGHT)
        )
        star_sprite.addPosRel(
            jovialengine.AnimSprite.Lerp,
            self.BACKGROUND_TIME,
            (-self.SPACE_WIDTH, 0)
        )
        self._background_sprites.add(star_sprite)

    def _update(self, dt: int):
        self._star_timer -= dt
        self._background_sprites.update(dt)
        if self._star_timer <= 0:
            for sprite in self._background_sprites:
                if not sprite.stillAnimating():
                    sprite.kill()
            self._star_timer = self.STAR_DELAY
            self._makeStar(self.SPACE_WIDTH)

        self._charge += dt * self.BAR_CHARGE_SPEED
        if self._charge > 1.0:
            self._charge = 1.0
        pass

    def _updatePreDraw(self, screen: pygame.surface.Surface):
        pass

    def _drawPreSprites(self, screen: pygame.surface.Surface):
        self._background_sprites.draw(screen)

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
