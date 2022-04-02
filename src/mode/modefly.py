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
    BAR_EMPTY_COLOR = (12, 24, 31)
    BAR_CHARGE_SPEED = 0.001 / 8
    STAR_DELAY = 25
    STAR_DISTANCE = SPACE_WIDTH + SPACE_BORDER * 2
    BACKGROUND_TIME = 2000
    SHAKES = (
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1),
    )
    __slots__ = (
        '_star_sprites_0',
        '_star_sprites_1',
        '_star_timer',
        '_star_image_0',
        '_star_image_1',
        '_bar_shake_timer',
        '_bar_shake',
        '_current_shake',
        '_charge',
        '_player_ship',
    )

    def __init__(self):
        self._init(self.SPACE_SIZE)
        self._camera = pygame.rect.Rect(
            self.SPACE_BORDER,
            self.SPACE_BORDER,
            self.SPACE_WIDTH - (self.SPACE_BORDER * 2),
            self.SPACE_HEIGHT - (self.SPACE_BORDER * 2)
        )
        self._background.fill(constants.BLACK)
        self._star_sprites_0 = pygame.sprite.Group()
        self._star_sprites_1 = pygame.sprite.Group()
        self._star_timer = self.STAR_DELAY
        self._star_image_0 = pygame.surface.Surface((3, 3)).convert()
        self._star_image_0.fill(constants.BLACK)
        self._star_image_0.fill(constants.WHITE, (0, 1, 3, 1))
        self._star_image_0.fill(constants.WHITE, (1, 0, 1, 3))
        self._star_image_1 = pygame.surface.Surface((1, 1)).convert()
        self._star_image_1.fill(constants.WHITE)

        stars = self.BACKGROUND_TIME // self.STAR_DELAY
        for s in range(stars):
            self._makeStar(
                int(self.SPACE_WIDTH * s / stars)
            )

        self._bar_shake_timer = None
        self._bar_shake = (0, 0)
        self._current_shake = None
        self._charge = 0.0
        self._player_ship = jovialengine.AnimSprite()
        self._player_ship.image = pygame.image.load(constants.SHIP).convert()
        self._player_ship.image.set_colorkey(constants.COLORKEY)
        self._player_ship.rect = self._player_ship.image.get_rect()
        self._player_ship.rect.midleft = (-self.SPACE_BORDER, self.SPACE_HEIGHT // 2)
        self._player_ship.addPosRel(
            jovialengine.AnimSprite.DecSpeed,
            self.BACKGROUND_TIME // 2,
            (self.SPACE_BORDER * 5, 0)
        )
        self._all_sprites.add(self._player_ship)
        # move other sprite to back? (to keep ship in front) self._all_sprites.move_to_back

    def _input(self, event: pygame.event.Event):
        if self._player_ship.stillAnimating():
            return
        # player movement, controls, etc

    def _makeStar(self, x):
        star_sprite_0 = jovialengine.AnimSprite()
        star_sprite_0.image = self._star_image_0
        star_sprite_0.rect = star_sprite_0.image.get_rect()
        star_sprite_0.rect.center = (
            x + random.randint(0, self.SPACE_BORDER),
            random.randint(0, self.SPACE_HEIGHT)
        )
        star_sprite_0.addPosRel(
            jovialengine.AnimSprite.Lerp,
            self.BACKGROUND_TIME,
            (-self.STAR_DISTANCE, 0)
        )
        self._star_sprites_0.add(star_sprite_0)
        star_sprite_1 = jovialengine.AnimSprite()
        star_sprite_1.image = self._star_image_1
        star_sprite_1.rect = star_sprite_1.image.get_rect()
        star_sprite_1.rect.center = (
            x + random.randint(0, self.SPACE_BORDER),
            random.randint(0, self.SPACE_HEIGHT)
        )
        star_sprite_1.addPosRel(
            jovialengine.AnimSprite.Lerp,
            self.BACKGROUND_TIME * 2,
            (-self.STAR_DISTANCE, 0)
        )
        self._star_sprites_1.add(star_sprite_1)

    def _setShake(self):
        if self._bar_shake == (0, 0):
            self._current_shake = random.randrange(len(self.SHAKES))
            self._bar_shake = self.SHAKES[self._current_shake]
        else:
            possible_shakes = list(range(len(self.SHAKES)))
            possible_shakes = possible_shakes[:self._current_shake] + possible_shakes[self._current_shake + 1:]
            self._current_shake = random.choice(possible_shakes)
            self._bar_shake = self.SHAKES[self._current_shake]

    def _update(self, dt: int):
        # background stars
        self._star_timer -= dt
        self._star_sprites_0.update(dt)
        self._star_sprites_1.update(dt)
        if self._star_timer <= 0:
            for sprite in self._star_sprites_0:
                if not sprite.stillAnimating():
                    sprite.kill()
            for sprite in self._star_sprites_1:
                if not sprite.stillAnimating():
                    sprite.kill()
            self._star_timer = self.STAR_DELAY
            self._makeStar(self.SPACE_WIDTH)

        self._charge += dt * self.BAR_CHARGE_SPEED
        if self._charge > 1.0:
            self._charge = 1.0

        # bar shaking
        if self._bar_shake_timer is not None:
            if self._bar_shake_timer > 0:
                self._bar_shake_timer -= dt
            if self._bar_shake_timer <= 0:
                self._bar_shake_timer = None
        if self._bar_shake_timer is None:
            if self._charge >= 0.75:
                self._bar_shake_timer = 125
                self._setShake()
            elif self._charge >= 0.5:
                self._bar_shake_timer = 250
                self._setShake()
            elif self._charge >= 0.25:
                self._bar_shake_timer = 500
                self._setShake()
            else:
                self._bar_shake = (0, 0)

    def _updatePreDraw(self, screen: pygame.surface.Surface):
        pass

    def _drawPreSprites(self, screen: pygame.surface.Surface):
        self._star_sprites_0.draw(screen)
        self._star_sprites_1.draw(screen)

    def _drawPostSprites(self, screen: pygame.surface.Surface):
        pass

    def _drawBarMarks(self, screen: pygame.surface.Surface, color, pos_x: int, width: int):
        screen.fill(
            color,
            (
                self.BAR_OFFSET + pos_x + self._bar_shake[0],
                constants.SCREEN_SIZE[1] - self.BAR_BORDER_HEIGHT + 1 + self._bar_shake[1],
                width,
                self.BAR_BORDER_HEIGHT - 2
            )
        )

    @staticmethod
    def _getBarColor(charge):
        bar_color_component = int(charge * 255)
        bar_color = (bar_color_component, 0, 255 - bar_color_component)
        return bar_color

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
        self._drawBarMarks(screen, self._getBarColor(0), 0, 3)
        # self._drawBarMarks(screen, constants.BLACK, 0, 1)
        self._drawBarMarks(screen, self._getBarColor(0.25), (self.BAR_WIDTH // 2) - (self.BAR_WIDTH // 4) - 2, 3)
        # self._drawBarMarks(screen, constants.BLACK, (self.BAR_WIDTH // 2) - (self.BAR_WIDTH // 4) - 1, 1)
        self._drawBarMarks(screen, self._getBarColor(0.5), (self.BAR_WIDTH // 2) - 2, 3)
        # self._drawBarMarks(screen, constants.BLACK, (self.BAR_WIDTH // 2) - 1, 1)
        self._drawBarMarks(screen, self._getBarColor(0.75), (self.BAR_WIDTH // 2) + (self.BAR_WIDTH // 4) - 2, 3)
        # self._drawBarMarks(screen, constants.BLACK, (self.BAR_WIDTH // 2) + (self.BAR_WIDTH // 4) - 1, 1)
        self._drawBarMarks(screen, self._getBarColor(1), self.BAR_WIDTH - 3, 3)
        # self._drawBarMarks(screen, constants.BLACK, self.BAR_WIDTH - 1, 1)
        # unfilled bar
        screen.fill(
            self.BAR_EMPTY_COLOR,
            (
                self.BAR_OFFSET + self._bar_shake[0],
                constants.SCREEN_SIZE[1] - self.BAR_BORDER_HEIGHT + self.BAR_OFFSET + self._bar_shake[1],
                self.BAR_WIDTH,
                self.BAR_HEIGHT
            )
        )
        # filled bar
        screen.fill(
            self._getBarColor(self._charge),
            (
                self.BAR_OFFSET + self._bar_shake[0],
                constants.SCREEN_SIZE[1] - self.BAR_BORDER_HEIGHT + self.BAR_OFFSET + self._bar_shake[1],
                self.BAR_WIDTH * self._charge,
                self.BAR_HEIGHT
            )
        )
