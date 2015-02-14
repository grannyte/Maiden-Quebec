# -*- coding: utf-8 -*-
from __future__ import print_function

from pygame.sprite import Sprite
from pygame import Rect


class Entity(Sprite):
    def __init__(self, x, y, tile_size):
        Sprite.__init__(self)
        self._colorkey = (0, 0, 0)
        self.tile_size = tile_size
        self.rect = Rect(x * tile_size, y * tile_size, tile_size, tile_size)