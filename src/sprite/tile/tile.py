# -*- coding: utf-8 -*-
from __future__ import print_function

from src.sprite.entity import Entity

from pygame import Rect


#TODO: Save memory, no need to have a img for each tile
class Tile(Entity):
    def __init__(self, x, y, tile_size, tile):
        Entity.__init__(self, x, y, tile_size)
        self.image = tile