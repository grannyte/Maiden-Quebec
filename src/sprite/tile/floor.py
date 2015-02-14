# -*- coding: utf-8 -*-
from __future__ import print_function

from src.sprite.tile.tile import Tile


#TODO: Save memory, no need to have a img for each tile
class Floor(Tile):
    def __init__(self, x, y, tile_size, tile, ):
        Tile.__init__(self, x, y, tile_size, tile)