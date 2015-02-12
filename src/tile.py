# -*- coding: utf-8 -*-
from pygame import *
from entity import Entity


class Tile(Entity):
    def __init__(self, x, y, spritesheet):
        Entity.__init__(self)
        self._spritesheet = spritesheet
        rect = (0*32, 1*32, 32, 32)
        self.image = self._spritesheet.image_at(rect)
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass

    def collide(self, p, xvel, yvel):
        pass