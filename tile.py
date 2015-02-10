# -*- coding: utf-8 -*-
from pygame import *
from entity import Entity


class Tile(Entity):
    def __init__(self, x, y, spritesheet):
        Entity.__init__(self)
        self._spritesheet = spritesheet
        rect = (3 * 64, 3 * 64, 64, 64)
        self.image = self._spritesheet.image_at(rect)
        self.rect = Rect(x, y, 64, 64)

    def update(self):
        pass

    def collide(self, p, xvel, yvel):
        pass