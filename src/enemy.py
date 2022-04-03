import random

import jovialengine
import pygame

import constants
import gameutility


class Enemy(jovialengine.AnimSprite):
    MOVEMENT_OPTIONS = (
        jovialengine.AnimSprite.IncSpeed,
        jovialengine.AnimSprite.DecSpeed,
        jovialengine.AnimSprite.IncDecSpeed,
        jovialengine.AnimSprite.DecIncSpeed,
    )

    __slots__ = (
        'sprite_group',
        'level',
    )

    def __init__(self, sprite_group: pygame.sprite.LayeredDirty, image, mask, level: int = 1):
        super().__init__()
        self.sprite_group = sprite_group
        self.level = min(4, level)
        fixed_image = image.copy()
        new_color = gameutility.getBarColor(level * 0.25)
        pix_array = pygame.PixelArray(fixed_image)
        pix_array.replace(
            constants.ENEMY_COLOR1,
            new_color
        )
        del pix_array
        self.image = fixed_image
        self.mask = mask
        self.rect = self.image.get_rect()
        self.rect.topleft = (672, random.randint(self.rect.height, 360 - self.rect.height * 2))
        if bool(random.getrandbits(1)):
            self.addPosRel(
                random.choice(self.MOVEMENT_OPTIONS),
                random.randint(1900, 2100),
                (-168, 0)
            )
        else:
            self.addPosAbs(
                random.choice(self.MOVEMENT_OPTIONS),
                random.randint(1900, 2100),
                (504, 180)
            )
        self.addPosAbs(
            random.choice(self.MOVEMENT_OPTIONS),
            random.randint(1450, 1550),
            (504, random.randint(16 + self.rect.height // 2, 360 - 16 - self.rect.height // 2)),
            callback=self._animCallback
        )

    def _animCallback(self):
        if self.rect.right < 0:
            self.kill()
        else:
            movement = random.choice(self.MOVEMENT_OPTIONS)
            timing = random.randint(1950, 2050)
            distance = random.randint(84, 168)
            self.addPosRel(
                movement,
                timing,
                (-168, 0),
                callback=self._animCallback
            )

    def update(self, *args):
        super().update(args[0])
        # shooting, maybe checking for death goes here?
        # lol might not get to projectiles
