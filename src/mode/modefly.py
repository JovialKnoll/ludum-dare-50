import abc
import random
import math

import pygame
import jovialengine

import constants
import gameutility
import mode
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
    BASE_CHARGE_SLOWDOWN_TIME = 500
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
    X_ACCEL = 1024 / 1000 / 1000
    X_SPEED_MAX = 320 / 1000
    X_DECEL = X_SPEED_MAX * 8 / 1000
    Y_ACCEL = 1024 / 1000 / 1000
    Y_SPEED_MAX = 288 / 1000
    Y_DECEL = X_DECEL
    MAX_BLAST_TIME = 1000 * 6
    BEAM_HALF_HEIGHT = 16
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
        '_spawn_timer',
        '_enemy_images',
        '_enemy_mask',
        '_enemy_count',
        '_enemy_group',
        '_kill_count_down',
        '_blast_kill_count',
        '_rao',
        '_bwom',
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
        ship_mask = pygame.image.load(constants.SHIP_MASK).convert()
        ship_mask.set_colorkey(constants.COLORKEY)
        self._player_ship.mask = pygame.mask.from_surface(ship_mask)
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

        self._spawn_timer = self._getSpawnWait() // 2
        enemy_image0 = pygame.image.load(constants.ENEMY0).convert()
        enemy_image0.set_colorkey(constants.COLORKEY)
        enemy_image1 = pygame.image.load(constants.ENEMY1).convert()
        enemy_image1.set_colorkey(constants.COLORKEY)
        enemy_image2 = pygame.image.load(constants.ENEMY2).convert()
        enemy_image2.set_colorkey(constants.COLORKEY)
        self._enemy_images = (enemy_image0, enemy_image1, enemy_image2)
        self._enemy_mask = pygame.mask.from_surface(enemy_image0)
        self._enemy_count = 0
        self._enemy_group = pygame.sprite.LayeredDirty()

        self._kill_count_down = self._getKillAmount()
        self._blast_kill_count = 0

        self._rao = pygame.mixer.Sound(constants.RAO)
        self._bwom = pygame.mixer.Sound(constants.BWOM)

    @abc.abstractmethod
    def _getSpawnWait(self):
        raise NotImplementedError(
            type(self).__name__ + "._getSpawnWait(self)"
        )

    @abc.abstractmethod
    def _getKillAmount(self):
        raise NotImplementedError(
            type(self).__name__ + "._getKillAmount(self)"
        )

    @abc.abstractmethod
    def _getEnemyLevel(self):
        raise NotImplementedError(
            type(self).__name__ + "._getEnemyLevel(self)"
        )

    def _failedBlast(self):
        self._stopMixer()
        self.next_mode = mode.ModeFailBlast()

    def _failedDied(self):
        self._stopMixer()
        self.next_mode = mode.ModeFailDeath()

    @abc.abstractmethod
    def _success(self):
        raise NotImplementedError(
            type(self).__name__ + "._success(self)"
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
        enemy = Enemy(self._all_sprites, random.choice(self._enemy_images), self._enemy_mask, self._getEnemyLevel())
        self._all_sprites.add(enemy)
        self._enemy_group.add(enemy)
        self._spawn_timer = self._getSpawnWait()
        self._enemy_count += 1

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
        return self._player_charge_slowdown_timer / (self.BASE_CHARGE_SLOWDOWN_TIME * 6)

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
            self._player_charge_slowdown_timer = min(
                self.BASE_CHARGE_SLOWDOWN_TIME * 6,
                self._player_charge_slowdown_timer + self.BASE_CHARGE_SLOWDOWN_TIME
            )
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
        if x_input == 0 and y_input == 0:
            self._player_charge_slowdown_timer -= dt * 5
        self._player_charge_slowdown_timer = max(0, self._player_charge_slowdown_timer)
        # end of blast
        old_blasting = self._blasting
        # blast countdown
        self._blasting -= dt
        self._blasting = max(0, self._blasting)
        if self._blasting == 0:
            # if just finished blasting
            if old_blasting > 0:
                self._bwom.stop()
                if self._blast_kill_count == 0:
                    self._failedBlast()
                elif self._kill_count_down <= 0:
                    self._stopMixer()
                    self._success()
                self._blast_kill_count = 0
            # charging
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
                charging_amount *= 3 / 4
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
                self._charge = 0
                self._bar_shake_timer = None
                self._player_charge_slowdown_timer = 0
                self._bwom.play()
            if self._bar_shake_timer is None:
                if self._charge < 0.25:
                    self._bar_shake = (0, 0)
                else:
                    self._bar_shake_timer = shake_timer_reset
                    self._setShake()
        # killing
        if self._blasting > 0:
            kill_sprites = [sprite for sprite in self._enemy_group if self._isSpriteDead(sprite)]
            for sprite in kill_sprites:
                sprite.kill()
        # check for death
        if pygame.sprite.spritecollideany(
            self._player_ship,
            self._enemy_group,
            collided=lambda sprite1, sprite2: pygame.sprite.collide_mask(sprite1, sprite2) is not None
        ):
            self._failedDied()
        # spawning
        self._spawn_timer -= dt
        self._spawn_timer = max(0, self._spawn_timer)
        if self._spawn_timer <= 0:
            self._spawnMonster()

    def _isSpriteDead(self, sprite: pygame.sprite.DirtySprite):
        level = self._getBlastLevel()
        is_enemy = isinstance(sprite, Enemy)
        if is_enemy and level < sprite.level:
            return False
        if sprite.rect.right <= self._player_ship.rect.right:
            # to left of start section
            return False
        # check straight line out from ship
        if sprite.rect.top > self._player_ship.rect.centery > sprite.rect.bottom:
            return True
        for i in range(level):
            size = level - i
            beam_rect = self._getBeamRect(size)
            result = self._isSpriteDeadSection(sprite, beam_rect, is_enemy, i + 1)
            if result is None:
                return False
            if result is True:
                if is_enemy:
                    self._kill_count_down -= 1
                    self._blast_kill_count += 1
                    self._rao.play()
                return True
        return False

    def _isSpriteDeadSection(self, sprite: pygame.sprite.DirtySprite, beam_rect: pygame.Rect, is_enemy: bool,
                             level: int):
        if is_enemy and level < sprite.level:
            return False
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
            if sprite.rect.right >= beam_rect.left:
                # touching main beam with right half of circle
                return True
        # inside start section
        return self._doesLineHitCircle(
            (
                self._player_ship.rect.right - 1,
                self._player_ship.rect.centery - 1,
            ),
            beam_rect.topleft,
            sprite.rect.center,
            sprite.rect.width // 2
        ) or self._doesLineHitCircle(
            (
                beam_rect.left,
                beam_rect.bottom - 1
            ),
            (
                self._player_ship.rect.right - 1,
                self._player_ship.rect.centery,
            ),
            sprite.rect.center,
            sprite.rect.width // 2
        )

    @staticmethod
    def _doesLineHitCircle(point1, point2, center, radius):
        x1, y1 = point1
        x2, y2 = point2
        x3, y3 = center
        dx, dy = x2 - x1, y2 - y1
        det = dx * dx + dy * dy
        a = (dy * (y3 - y1) + dx * (x3 - x1)) / det
        closest_point = (x1 + a * dx, y1 + a * dy)
        return math.dist(closest_point, center) <= radius

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
        if self._blasting > 0:
            level = self._getBlastLevel()
            for i in range(level):
                size = level - i
                color = gameutility.getBarColor((i + 1) * 0.25)
                beam_rect = self._getBeamRect(size)
                pygame.draw.polygon(
                    screen,
                    color,
                    (
                        (
                            self._player_ship.rect.right - 1,
                            self._player_ship.rect.centery - 1,
                        ),
                        beam_rect.topleft,
                        (
                            beam_rect.left,
                            beam_rect.bottom - 1
                        ),
                        (
                            self._player_ship.rect.right - 1,
                            self._player_ship.rect.centery,
                        ),
                    )
                )
                screen.fill(color, beam_rect.clip(screen.get_rect()))

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
        pass

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
        jovialengine.shared.font_wrap.renderTo(
            screen,
            (0, 0),
            "ENEMIES LEFT IN WAVE: " + str(max(0, self._kill_count_down)),
            constants.WHITE
        )
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
            text = str(self._blast_kill_count) + " HIT COMBO"
            text_width = jovialengine.shared.font_wrap.font.size(text)[0]
            jovialengine.shared.font_wrap.renderTo(
                screen,
                (constants.SCREEN_SIZE[0] - text_width - 4, 0),
                text,
                constants.WHITE
            )
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
