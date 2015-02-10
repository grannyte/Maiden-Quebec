# -*- coding: utf-8 -*-
import pygame
from pygame import *

from entity import Entity


class Character(Entity):
    def __init__(self, x, y, spritesheet):
        Entity.__init__(self)

        self._parse_spritesheet(spritesheet)
        self.rect = Rect(x, y, 64, 64)
        self._heading = pygame.math.Vector2(0, 0)
        # actions
        self._is_standing_still = True
        self._frame = 0
        self._action = 'walk'
        self._facing = '_south'
        self._animations = self._spritesheet[self._action + self._facing]
        self.ticks = 0
        self._last_action = ''

    def update(self, platforms, since_last_tick):
        if self._is_standing_still:
            self.image = self._spritesheet[self._action + self._facing][0]
        elif self.ticks == 0:  # The action was approved during control test
            self.image = self._animations[self._frame]
            self._frame += 1
            self._frame %= len(self._animations)
            self.rect.left += self._heading.x
            self.rect.top += self._heading.y
            self.collide(self._heading.x, self._heading.y, platforms)

    # TODO: Améliorer la détection des colisions
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                p.collide(self, xvel, yvel)

    def _parse_spritesheet(self, spritesheet):
        """
        Loads up an character's sprite (heroes or enemies)in a dict
        spritesheet must have a height of 21*64 pixels and a width of 13*64 pixel
        """
        colorkey = (0, 0, 0)
        self._spritesheet = {}
        # cast
        rects = [Rect(x, 0, 64, 64) for x in range(0, 7 * 64, 64)]
        self._spritesheet['cast_north'] = spritesheet.images_at(rects, colorkey)
        rects = [Rect(x, 1 * 64, 64, 64) for x in range(0, 7 * 64, 64)]
        self._spritesheet['cast_west'] = spritesheet.images_at(rects, colorkey)
        rects = [Rect(x, 2 * 64, 64, 64) for x in range(0, 7 * 64, 64)]
        self._spritesheet['cast_south'] = spritesheet.images_at(rects, colorkey)
        rects = [Rect(x, 3 * 64, 64, 64) for x in range(0, 7 * 64, 64)]
        self._spritesheet['cast_est'] = spritesheet.images_at(rects, colorkey)
        # spear thrust
        rects = [Rect(x, 4 * 64, 64, 64) for x in range(0, 8 * 64, 64)]
        self._spritesheet['thrust_north'] = spritesheet.images_at(rects, colorkey)
        rects = [Rect(x, 5 * 64, 64, 64) for x in range(0, 8 * 64, 64)]
        self._spritesheet['thrust_west'] = spritesheet.images_at(rects, colorkey)
        rects = [Rect(x, 6 * 64, 64, 64) for x in range(0, 8 * 64, 64)]
        self._spritesheet['thrust_south'] = spritesheet.images_at(rects, colorkey)
        rects = [Rect(x, 7 * 64, 64, 64) for x in range(0, 8 * 64, 64)]
        self._spritesheet['thrust_est'] = spritesheet.images_at(rects, colorkey)
        # walk
        rects = [Rect(x, 8 * 64, 64, 64) for x in range(0, 9 * 64, 64)]
        self._spritesheet['walk_north'] = spritesheet.images_at(rects, colorkey)
        rects = [Rect(x, 9 * 64, 64, 64) for x in range(0, 9 * 64, 64)]
        self._spritesheet['walk_west'] = spritesheet.images_at(rects, colorkey)
        rects = [Rect(x, 10 * 64, 64, 64) for x in range(0, 9 * 64, 64)]
        self._spritesheet['walk_south'] = spritesheet.images_at(rects, colorkey)
        rects = [Rect(x, 11 * 64, 64, 64) for x in range(0, 9 * 64, 64)]
        self._spritesheet['walk_est'] = spritesheet.images_at(rects, colorkey)
        # attack
        rects = [Rect(x, 12 * 64, 64, 64) for x in range(0, 6 * 64, 64)]
        self._spritesheet['attack_north'] = spritesheet.images_at(rects, colorkey)
        rects = [Rect(x, 13 * 64, 64, 64) for x in range(0, 6 * 64, 64)]
        self._spritesheet['attack_west'] = spritesheet.images_at(rects, colorkey)
        rects = [Rect(x, 14 * 64, 64, 64) for x in range(0, 6 * 64, 64)]
        self._spritesheet['attack_south'] = spritesheet.images_at(rects, colorkey)
        rects = [Rect(x, 15 * 64, 64, 64) for x in range(0, 6 * 64, 64)]
        self._spritesheet['attack_est'] = spritesheet.images_at(rects, colorkey)
        # bow
        rects = [Rect(x, 12 * 64, 64, 64) for x in range(0, 13 * 64, 64)]
        self._spritesheet['bow_north'] = spritesheet.images_at(rects, colorkey)
        rects = [Rect(x, 13 * 64, 64, 64) for x in range(0, 13 * 64, 64)]
        self._spritesheet['bow_west'] = spritesheet.images_at(rects, colorkey)
        rects = [Rect(x, 14 * 64, 64, 64) for x in range(0, 13 * 64, 64)]
        self._spritesheet['bow_south'] = spritesheet.images_at(rects, colorkey)
        rects = [Rect(x, 15 * 64, 64, 64) for x in range(0, 13 * 64, 64)]
        self._spritesheet['bow_est'] = spritesheet.images_at(rects, colorkey)
        # die
        rects = [Rect(x, 12 * 64, 64, 64) for x in range(0, 6 * 64, 64)]
        self._spritesheet['die_south'] = spritesheet.images_at(rects, colorkey)