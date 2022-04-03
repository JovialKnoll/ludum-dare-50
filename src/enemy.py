import sys
import os
import random

import jovialengine
import pygame.sprite


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

    def __init__(self, sprite_group: pygame.sprite.LayeredDirty, image, level: int = 1):
        super().__init__()
        self.sprite_group = sprite_group
        self.level = min(4, level)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (672, random.randint(self.rect.height, 360 - self.rect.height * 2))
        if bool(random.getrandbits(1)):
            self.addPosRel(
                random.choice(self.MOVEMENT_OPTIONS),
                random.randint(900, 1100),
                (-168, 0)
            )
        else:
            self.addPosAbs(
                random.choice(self.MOVEMENT_OPTIONS),
                random.randint(900, 1100),
                (504, 180)
            )
        self.addPosAbs(
            random.choice(self.MOVEMENT_OPTIONS),
            random.randint(450, 550),
            (504, random.randint(16 + self.rect.height // 2, 360 - 16 - self.rect.height // 2)),
            callback=self._animCallback
        )

    def _animCallback(self):
        if self.rect.right < 0:
            self.kill()
        else:
            movement = random.choice(self.MOVEMENT_OPTIONS)
            timing = random.randint(950, 1050)
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
