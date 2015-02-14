# -*- coding: utf-8 -*-
from __future__ import print_function


class Map(object):
    def __init__(self):
        self._sprite_sheet = {}
        self._tile_size = 64
        self._colorkey = (0, 0, 0)
        self._tiles = []