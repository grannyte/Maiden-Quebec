# -*- coding: utf-8 -*-
from __future__ import print_function

from os.path import join

from src.sprite.entity import Entity
from src.sprite.spritesheet import Spritesheet
from pygame import Rect


class LifeForm(Entity):
    def __init__(self, x, y, tile_size, appearance_sprite_sheet_file):
        Entity.__init__(self, x, y, tile_size)
        #self.rect = Rect(x, y, self.tile_size, self.tile_size)
        self._sprite_sheet = {}
        # TODO: remove default appearance
        self._change_appearance(appearance_sprite_sheet_file, self.tile_size)
        self.image = self._sprite_sheet['walk_south'][0]

    def _change_appearance(self, spritesheet_path, tile_size):
        """
        Changes the appearance of the living  thing according to the spritesheet's specifications.
        :param spritesheet_path: width:13*tile_size, height:21*tile_size spritesheet
        :return:
        """
        spritesheet = Spritesheet(spritesheet_path)
        actions = [('cast', 7), ('thrust', 8), ('walk', 9), ('attack', 6), ('bow', 13), ('die', 6)]
        cardinals = ['_north', '_west', '_south', '_east']

        # cast
        rects = [Rect(x, 0, tile_size, tile_size) for x in range(0, 7 * tile_size, tile_size)]
        self._sprite_sheet['cast_north'] = spritesheet.images_at(rects, self._colorkey)
        rects = [Rect(x, 1 * tile_size, tile_size, tile_size) for x in range(0, 7 * tile_size, tile_size)]
        self._sprite_sheet['cast_west'] = spritesheet.images_at(rects, self._colorkey)
        rects = [Rect(x, 2 * tile_size, tile_size, tile_size) for x in range(0, 7 * tile_size, tile_size)]
        self._sprite_sheet['cast_south'] = spritesheet.images_at(rects, self._colorkey)
        rects = [Rect(x, 3 * tile_size, tile_size, tile_size) for x in range(0, 7 * tile_size, tile_size)]
        self._sprite_sheet['cast_est'] = spritesheet.images_at(rects, self._colorkey)
        # spear thrust
        rects = [Rect(x, 4 * tile_size, tile_size, tile_size) for x in range(0, 8 * tile_size, tile_size)]
        self._sprite_sheet['thrust_north'] = spritesheet.images_at(rects, self._colorkey)
        rects = [Rect(x, 5 * tile_size, tile_size, tile_size) for x in range(0, 8 * tile_size, tile_size)]
        self._sprite_sheet['thrust_west'] = spritesheet.images_at(rects, self._colorkey)
        rects = [Rect(x, 6 * tile_size, tile_size, tile_size) for x in range(0, 8 * tile_size, tile_size)]
        self._sprite_sheet['thrust_south'] = spritesheet.images_at(rects, self._colorkey)
        rects = [Rect(x, 7 * tile_size, tile_size, tile_size) for x in range(0, 8 * tile_size, tile_size)]
        self._sprite_sheet['thrust_est'] = spritesheet.images_at(rects, self._colorkey)
        # walk
        rects = [Rect(x, 8 * tile_size, tile_size, tile_size) for x in range(0, 9 * tile_size, tile_size)]
        self._sprite_sheet['walk_north'] = spritesheet.images_at(rects, self._colorkey)
        rects = [Rect(x, 9 * tile_size, tile_size, tile_size) for x in range(0, 9 * tile_size, tile_size)]
        self._sprite_sheet['walk_west'] = spritesheet.images_at(rects, self._colorkey)
        rects = [Rect(x, 10 * tile_size, tile_size, tile_size) for x in range(0, 9 * tile_size, tile_size)]
        self._sprite_sheet['walk_south'] = spritesheet.images_at(rects, self._colorkey)
        rects = [Rect(x, 11 * tile_size, tile_size, tile_size) for x in range(0, 9 * tile_size, tile_size)]
        self._sprite_sheet['walk_est'] = spritesheet.images_at(rects, self._colorkey)
        # attack
        rects = [Rect(x, 12 * tile_size, tile_size, tile_size) for x in range(0, 6 * tile_size, tile_size)]
        self._sprite_sheet['attack_north'] = spritesheet.images_at(rects, self._colorkey)
        rects = [Rect(x, 13 * tile_size, tile_size, tile_size) for x in range(0, 6 * tile_size, tile_size)]
        self._sprite_sheet['attack_west'] = spritesheet.images_at(rects, self._colorkey)
        rects = [Rect(x, 14 * tile_size, tile_size, tile_size) for x in range(0, 6 * tile_size, tile_size)]
        self._sprite_sheet['attack_south'] = spritesheet.images_at(rects, self._colorkey)
        rects = [Rect(x, 15 * tile_size, tile_size, tile_size) for x in range(0, 6 * tile_size, tile_size)]
        self._sprite_sheet['attack_est'] = spritesheet.images_at(rects, self._colorkey)
        # bow
        rects = [Rect(x, 12 * tile_size, tile_size, tile_size) for x in range(0, 13 * tile_size, tile_size)]
        self._sprite_sheet['bow_north'] = spritesheet.images_at(rects, self._colorkey)
        rects = [Rect(x, 13 * tile_size, tile_size, tile_size) for x in range(0, 13 * tile_size, tile_size)]
        self._sprite_sheet['bow_west'] = spritesheet.images_at(rects, self._colorkey)
        rects = [Rect(x, 14 * tile_size, tile_size, tile_size) for x in range(0, 13 * tile_size, tile_size)]
        self._sprite_sheet['bow_south'] = spritesheet.images_at(rects, self._colorkey)
        rects = [Rect(x, 15 * tile_size, tile_size, tile_size) for x in range(0, 13 * tile_size, tile_size)]
        self._sprite_sheet['bow_est'] = spritesheet.images_at(rects, self._colorkey)
        # die
        rects = [Rect(x, 12 * tile_size, tile_size, tile_size) for x in range(0, 6 * tile_size, tile_size)]
        self._sprite_sheet['die_south'] = spritesheet.images_at(rects, self._colorkey)