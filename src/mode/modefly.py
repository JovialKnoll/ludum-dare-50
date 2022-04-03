import abc
import random

import pygame
import jovialengine

import constants
import gameutility
from enemy import Enemy


class ModeFly(jovialengine.ModeBase, abc.ABC):
    SPACE_WIDTH = 672
    SPACE_HEIGHT = 360
    SPACE_SIZE = (SPACE_WIDTH, SPACE_HEIGHT)
    SPACE_BORDER = 16
    BAR_WIDTH = 632
    BAR_HEIGHT = 24
    BAR_BORDER_HEIGHT = 32
    BAR_OFFSET = (BAR_BORDER_HEIGHT - BAR_HEIGHT) // 2
    BAR_BORDER_COLOR = (15, 15, 25)
    BAR_EMPTY_COLOR = (4, 6, 8)
    BAR_SLOWDOWN_COLOR = (100, 220, 100)
    BASE_CHARGE_SPEED = 1 / 16000
    BASE_CHARGE_SLOWDOWN_TIME = 1000
    STAR_DELAY = 200
    STAR_DISTANCE = SPACE_WIDTH + SPACE_BORDER * 2
    BACKGROUND_TIME = 16000
    SHAKES = (
        (-1, -1),
        (-1, 1),
        (1, -1),
        (1, 1),
    )
    KEYS_LEFT = {pygame.K_LEFT, pygame.K_a}
    KEYS_RIGHT = {pygame.K_RIGHT, pygame.K_d}
    KEYS_UP = {pygame.K_UP, pygame.K_w}
    KEYS_DOWN = {pygame.K_DOWN, pygame.K_s}
    X_ACCEL = 64 / 1000 / 125
    X_SPEED_MAX = 320 / 1000
    X_DECEL = X_SPEED_MAX / 125
    Y_ACCEL = 64 / 1000 / 125
    Y_SPEED_MAX = 288 / 1000
    Y_DECEL = X_DECEL
    MAX_BLAST_TIME = 1000 * 6
    BEAM_HALF_HEIGHT = 32
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
        '_player_input',
        '_prev_x_input',
        '_prev_y_input',
        '_player_vel_x',
        '_player_vel_y',
        '_player_x',
        '_player_y',
        '_player_charge_slowdown_timer',
        '_blasting',
        '_can_blast',
        '_spawn_timer',
        '_enemy_images',
        '_enemy_level',
        '_enemy_count',
        '_kill_count',
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
            500,
            (self.SPACE_BORDER * 5, 0),
            callback=self._syncPos
        )
        self._all_sprites.add(self._player_ship)
        # move other sprite to back? (to keep ship in front) self._all_sprites.move_to_back
        self._player_input = {
            'left': 0,
            'right': 0,
            'up': 0,
            'down': 0,
        }
        self._prev_x_input = 0
        self._prev_y_input = 0
        self._player_vel_x = 0.0
        self._player_vel_y = 0.0
        self._player_x = 0
        self._player_y = 0
        self._player_charge_slowdown_timer = 0

        self._blasting = 0
        self._can_blast = True

        self._spawn_timer = self._getSpawnWait() // 2
        enemy_image0 = pygame.image.load(constants.ENEMY0).convert()
        enemy_image0.set_colorkey(constants.COLORKEY)
        enemy_image1 = pygame.image.load(constants.ENEMY1).convert()
        enemy_image1.set_colorkey(constants.COLORKEY)
        enemy_image2 = pygame.image.load(constants.ENEMY2).convert()
        enemy_image2.set_colorkey(constants.COLORKEY)
        self._enemy_images = (enemy_image0, enemy_image1, enemy_image2)
        self._enemy_level = 1
        self._enemy_count = 0
        self._kill_count = 0

    @abc.abstractmethod
    def _getSpawnWait(self):
        raise NotImplementedError(
            type(self).__name__ + "._getSpawnWait(self)"
        )

    def _syncPos(self):
        self._player_x = float(self._player_ship.rect.x)
        self._player_y = float(self._player_ship.rect.y)

    def _input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.KEYS_LEFT:
                self._player_input['left'] = 1
            elif event.key in self.KEYS_RIGHT:
                self._player_input['right'] = 1
            elif event.key in self.KEYS_UP:
                self._player_input['up'] = 1
            elif event.key in self.KEYS_DOWN:
                self._player_input['down'] = 1
            # testing
            elif event.key == pygame.K_1:
                self._can_blast = True
                self._player_charge_slowdown_timer = 0
                self._charge = 0.2499
            elif event.key == pygame.K_2:
                self._can_blast = True
                self._player_charge_slowdown_timer = 0
                self._charge = 0.4999
            elif event.key == pygame.K_3:
                self._can_blast = True
                self._player_charge_slowdown_timer = 0
                self._charge = 0.7499
            elif event.key == pygame.K_4:
                self._can_blast = True
                self._player_charge_slowdown_timer = 0
                self._charge = 0.9999
        elif event.type == pygame.KEYUP:
            if event.key in self.KEYS_LEFT:
                self._player_input['left'] = 0
            elif event.key in self.KEYS_RIGHT:
                self._player_input['right'] = 0
            elif event.key in self.KEYS_UP:
                self._player_input['up'] = 0
            elif event.key in self.KEYS_DOWN:
                self._player_input['down'] = 0
        elif event.type == pygame.JOYAXISMOTION:
            if event.axis in (0, 2):
                self._player_input['left'] = 0
                self._player_input['right'] = 0
                if event.value < -0.3:
                    self._player_input['left'] = 1
                elif event.value > 0.3:
                    self._player_input['right'] = 1
            elif event.axis in (1, 3):
                self._player_input['up'] = 0
                self._player_input['down'] = 0
                if event.value < -0.3:
                    self._player_input['up'] = 1
                elif event.value > 0.3:
                    self._player_input['down'] = 1
        elif event.type == pygame.JOYHATMOTION:
            self._player_input['left'] = 0
            self._player_input['right'] = 0
            self._player_input['up'] = 0
            self._player_input['down'] = 0
            if event.value[0] == -1:
                self._player_input['left'] = 1
            elif event.value[0] == 1:
                self._player_input['right'] = 1
            if event.value[1] == 1:
                self._player_input['up'] = 1
            elif event.value[1] == -1:
                self._player_input['down'] = 1

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

    def _spawnMonster(self):
        level = self._enemy_level
        if random.random() < 0.15:
            level = min(4, level + 1)
        enemy = Enemy(self._all_sprites, random.choice(self._enemy_images), level)
        self._all_sprites.add(enemy)
        self._enemy_count += 1
        if self._enemy_count == 8:
            self._enemy_level = 2
        elif self._enemy_count == 16:
            self._enemy_level = 3
        elif self._enemy_count == 24:
            self._enemy_level = 4
        elif self._enemy_count == 30:
            # win against this wave?
            pass
        self._spawn_timer = self._getSpawnWait()

    def _setShake(self):
        if self._bar_shake == (0, 0):
            self._current_shake = random.randrange(len(self.SHAKES))
            self._bar_shake = self.SHAKES[self._current_shake]
        else:
            possible_shakes = list(range(len(self.SHAKES)))
            possible_shakes = possible_shakes[:self._current_shake] + possible_shakes[self._current_shake + 1:]
            self._current_shake = random.choice(possible_shakes)
            self._bar_shake = self.SHAKES[self._current_shake]

    def _getSlowdownAmount(self):
        return self._player_charge_slowdown_timer / self.BASE_CHARGE_SLOWDOWN_TIME

    def _update(self, dt):
        # background stars
        self._star_timer -= dt
        self._star_sprites_0.update(dt)
        self._star_sprites_1.update(dt)
        if self._player_ship.stillAnimating():
            # can only do player movement after it animated into place
            return
        # player movement
        # apply accel or decel based on input
        x_input = self._player_input['right'] - self._player_input['left']
        x_decel = self.X_DECEL * dt
        if x_input == 0:
            if self._player_vel_x > x_decel:
                self._player_vel_x -= x_decel
            elif self._player_vel_x < -x_decel:
                self._player_vel_x += x_decel
            else:
                self._player_vel_x = 0.0
        else:
            if x_input == -1 and self._player_vel_x > 0:
                self._player_vel_x = max(0.0, self._player_vel_x - x_decel)
            elif x_input == 1 and self._player_vel_x < 0:
                self._player_vel_x = min(0.0, self._player_vel_x + x_decel)
            self._player_vel_x += x_input * self.X_ACCEL * dt
        y_input = self._player_input['down'] - self._player_input['up']
        y_decel = self.Y_DECEL * dt
        if y_input == 0:
            if self._player_vel_y > y_decel:
                self._player_vel_y -= y_decel
            elif self._player_vel_y < -y_decel:
                self._player_vel_y += y_decel
            else:
                self._player_vel_y = 0.0
        else:
            if y_input == -1 and self._player_vel_y > 0:
                self._player_vel_y = max(0.0, self._player_vel_y - y_decel)
            elif y_input == 1 and self._player_vel_y < 0:
                self._player_vel_y = min(0.0, self._player_vel_y + y_decel)
            self._player_vel_y += y_input * self.Y_ACCEL * dt
        if self._prev_x_input != x_input or self._prev_y_input != y_input:
            self._player_charge_slowdown_timer = self.BASE_CHARGE_SLOWDOWN_TIME
            self._prev_x_input = x_input
            self._prev_y_input = y_input
        # cap velocity
        self._player_vel_x = max(-self.X_SPEED_MAX, min(self.X_SPEED_MAX, self._player_vel_x))
        self._player_vel_y = max(-self.Y_SPEED_MAX, min(self.Y_SPEED_MAX, self._player_vel_y))
        # apply velocity
        self._player_x += self._player_vel_x * dt
        self._player_y += self._player_vel_y * dt
        # cap position
        self._player_x = max(
            self.SPACE_BORDER,
            min(
                self.SPACE_WIDTH - self.SPACE_BORDER - self._player_ship.rect.width,
                self._player_x
            )
        )
        self._player_y = max(
            self.SPACE_BORDER,
            min(
                self.SPACE_HEIGHT - self.SPACE_BORDER - self._player_ship.rect.height,
                self._player_y
            )
        )
        # apply position to player rect
        self._player_ship.rect.x = int(self._player_x)
        self._player_ship.rect.y = int(self._player_y)
        # charge slowdown
        self._player_charge_slowdown_timer -= dt
        self._player_charge_slowdown_timer = max(0, self._player_charge_slowdown_timer)
        # charging
        self._blasting -= dt
        self._blasting = max(0, self._blasting)
        if self._can_blast:
            threshold = 0.0
            shake_timer_reset = 0
            if self._charge < 0.25:
                threshold = 0.25
                shake_timer_reset = 0
            elif self._charge < 0.5:
                threshold = 0.5
                shake_timer_reset = 400
            elif self._charge < 0.75:
                threshold = 0.75
                shake_timer_reset = 200
            elif self._charge < 1.0:
                threshold = 1.0
                shake_timer_reset = 100
            charging_amount = dt * self.BASE_CHARGE_SPEED
            if self._getSlowdownAmount() >= threshold:
                charging_amount /= 2
                shake_timer_reset *= 2
            elif self._player_charge_slowdown_timer > 0:
                charging_amount *= 3/4
                shake_timer_reset = shake_timer_reset + shake_timer_reset // 2
            self._charge = min(1.0, self._charge + charging_amount)
            if self._bar_shake_timer is not None:
                if self._bar_shake_timer > 0:
                    self._bar_shake_timer -= dt
                if self._bar_shake_timer <= 0:
                    self._bar_shake_timer = None
            if self._charge >= threshold > self._getSlowdownAmount():
                # kick off blast here
                self._blasting = int(threshold * self.MAX_BLAST_TIME)
                self._can_blast = False
                self._charge = 0
                self._bar_shake_timer = None
                self._player_charge_slowdown_timer = 0
            if self._bar_shake_timer is None:
                if self._charge < 0.25:
                    self._bar_shake = (0, 0)
                else:
                    self._bar_shake_timer = shake_timer_reset
                    self._setShake()
        # spawning
        self._spawn_timer -= dt
        self._spawn_timer = max(0, self._spawn_timer)
        if self._spawn_timer <= 0:
            self._spawnMonster()
        # killing
        if self._blasting > 0:
            level = self._getBlastLevel()
            kill_sprites = [sprite for sprite in self._all_sprites if self._isSpriteDead(sprite, level)]
            for sprite in kill_sprites:
                sprite.kill()
        # somehow self._can_blast must be set true again later

    def _isSpriteDead(self, sprite: pygame.sprite.DirtySprite, level: int):
        #self._kill_count
        is_enemy = isinstance(sprite, Enemy)
        if is_enemy and sprite.level > level:
            return False
        if self._player_ship.rect.right > sprite.rect.right:
            # to left of start of beam
            return False
        beam_rect = self._getBeamRect(level)
        result = self._isSpriteDeadSection(sprite, beam_rect, is_enemy)
        if result is None:
            return False
        if result is True:
            if is_enemy:
                self._kill_count += 1
            return True
        for i in range(7):
            # distance from player = self.BEAM_HALF_HEIGHT * 2
            new_rect = pygame.Rect(
                # 1 / 8th closer per iteration
                beam_rect.x - self.BEAM_HALF_HEIGHT // 4 * (1 + i),
                beam_rect.y + beam_rect.height // 16 * (1 + i),
                beam_rect.width,
                beam_rect.height - beam_rect.height // 8 * (1 + i),
            )
            result = self._isSpriteDeadSection(sprite, new_rect, is_enemy)
            if result is None:
                return False
            if result is True:
                if is_enemy:
                    self._kill_count += 1
                return True
        return False

    @staticmethod
    def _isSpriteDeadSection(sprite: pygame.sprite.DirtySprite, beam_rect: pygame.Rect, is_enemy: bool):
        # right is to right of beam start
        if sprite.rect.bottom <= beam_rect.top or sprite.rect.top >= beam_rect.bottom:
            # entirely outside of beam top and bottom
            return None
        if sprite.rect.centerx >= beam_rect.left:
            # center is to right of main beam
            return True
        # center is to left of main beam
        if beam_rect.top > sprite.rect.centery > beam_rect.bottom:
            # center is within beam start section
            if not is_enemy:
                # this is close enough to destroy bullets
                return True
            if sprite.rect.right > beam_rect.left:
                # touching main beam with right half of circle
                return True
        return False

    def _updatePreDraw(self, screen):
        # star one-per-frame updates
        if self._star_timer <= 0:
            for sprite in self._star_sprites_0:
                if not sprite.stillAnimating():
                    sprite.kill()
            for sprite in self._star_sprites_1:
                if not sprite.stillAnimating():
                    sprite.kill()
            self._star_timer = self.STAR_DELAY
            self._makeStar(self.SPACE_WIDTH)

    def _drawPreSprites(self, screen):
        self._star_sprites_0.draw(screen)
        self._star_sprites_1.draw(screen)

    def _getBlastLevel(self):
        return 1 + (self._blasting - 1) * 4 // self.MAX_BLAST_TIME

    def _getBeamRect(self, size: int):
        return pygame.Rect(
            self._player_ship.rect.right + self.BEAM_HALF_HEIGHT * 2,
            self._player_ship.rect.centery - self.BEAM_HALF_HEIGHT * size,
            self.SPACE_WIDTH - self._player_ship.rect.right - self.BEAM_HALF_HEIGHT * 2,
            self.BEAM_HALF_HEIGHT * 2 * size
        )

    def _drawPostSprites(self, screen):
        if self._blasting > 0:
            level = self._getBlastLevel()
            for i in range(level):
                size = level - i
                color = gameutility.getBarColor((i + 1) * 0.25)
                pygame.draw.polygon(
                    screen,
                    color,
                    (
                        (
                            self._player_ship.rect.right - 1,
                            self._player_ship.rect.centery - 1,
                        ),
                        (
                            self._player_ship.rect.right + self.BEAM_HALF_HEIGHT * 2,
                            self._player_ship.rect.centery - self.BEAM_HALF_HEIGHT * size
                        ),
                        (
                            self._player_ship.rect.right + self.BEAM_HALF_HEIGHT * 2,
                            self._player_ship.rect.centery + self.BEAM_HALF_HEIGHT * size - 1
                        ),
                        (
                            self._player_ship.rect.right - 1,
                            self._player_ship.rect.centery,
                        ),
                    )
                )
                screen.fill(color, self._getBeamRect(size))

    def _drawBarMarks(self, screen: pygame.surface.Surface, color, pos_x: int, width: int):
        screen.fill(
            color,
            (
                self.BAR_OFFSET + pos_x + self._bar_shake[0],
                constants.SCREEN_SIZE[1] - self.BAR_BORDER_HEIGHT,
                width,
                self.BAR_BORDER_HEIGHT
            )
        )

    def _drawPostCamera(self, screen):
        draw_safety_marks = False
        visible_charge = max(0.0, self._charge)
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
        if self._blasting > 0:
            visible_charge = self._blasting / self.MAX_BLAST_TIME
        else:
            # slowdown bar
            screen.fill(
                self.BAR_SLOWDOWN_COLOR,
                (
                    self.BAR_OFFSET + self._bar_shake[0],
                    constants.SCREEN_SIZE[1] - self.BAR_BORDER_HEIGHT,
                    self.BAR_WIDTH * self._getSlowdownAmount(),
                    self.BAR_BORDER_HEIGHT
                )
            )
            if self._charge < 0.25:
                draw_safety_marks = self._getSlowdownAmount() >= 0.25
            elif self._charge < 0.5:
                draw_safety_marks = self._getSlowdownAmount() >= 0.5
            elif self._charge < 0.75:
                draw_safety_marks = self._getSlowdownAmount() >= 0.75
        if draw_safety_marks:
            screen.fill(
                self.BAR_SLOWDOWN_COLOR,
                (
                    0,
                    constants.SCREEN_SIZE[1] - self.BAR_BORDER_HEIGHT,
                    self.BAR_OFFSET + 1,
                    self.BAR_BORDER_HEIGHT
                )
            )
            screen.fill(
                self.BAR_SLOWDOWN_COLOR,
                (
                    self.BAR_OFFSET + self.BAR_WIDTH - 1,
                    constants.SCREEN_SIZE[1] - self.BAR_BORDER_HEIGHT,
                    self.BAR_OFFSET + 1,
                    self.BAR_BORDER_HEIGHT
                )
            )
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
            gameutility.getBarColor(visible_charge),
            (
                self.BAR_OFFSET + self._bar_shake[0],
                constants.SCREEN_SIZE[1] - self.BAR_BORDER_HEIGHT + self.BAR_OFFSET + self._bar_shake[1],
                self.BAR_WIDTH * max(0.0, visible_charge),
                self.BAR_HEIGHT
            )
        )
        self._drawBarMarks(screen, gameutility.getBarColor(0), 0, 3)
        self._drawBarMarks(screen, gameutility.getBarColor(0.25), (self.BAR_WIDTH // 2) - (self.BAR_WIDTH // 4) - 2, 3)
        self._drawBarMarks(screen, gameutility.getBarColor(0.5), (self.BAR_WIDTH // 2) - 2, 3)
        self._drawBarMarks(screen, gameutility.getBarColor(0.75), (self.BAR_WIDTH // 2) + (self.BAR_WIDTH // 4) - 2, 3)
        self._drawBarMarks(screen, gameutility.getBarColor(1), self.BAR_WIDTH - 3, 3)
        jovialengine.shared.font_wrap.renderTo(
            screen,
            (0, 0),
            "KILL COUNT: " + str(self._kill_count),
            constants.WHITE
        )
