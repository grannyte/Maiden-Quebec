# -*- coding: utf-8 -*-
from __future__ import print_function

from pygame import Rect

from os.path import join

from src.map.map import Map
from src.sprite.tile import tile, door, floor, wall
from src.sprite.spritesheet import Spritesheet


class Temple(Map):
    """
    The temple is the initial place where the players appears.  It is also the place they pop out when they die
    """
    def __init__(self, project_dir):
        Map.__init__(self)
        self._parse_sprite_sheet(join(project_dir, 'data', 'img', 'temple.png'))
        self._build()

    def _parse_sprite_sheet(self, sprite_sheet_file):
        """
        Build the map
        :return:
        """
        sprite_sheet = Spritesheet(sprite_sheet_file)
        door = Rect(0, 0, self._tile_size, self._tile_size)
        wall = Rect(3 * self._tile_size, 1 * self._tile_size, self._tile_size, self._tile_size)
        floor = Rect(3 * self._tile_size, 2 * self._tile_size, self._tile_size, self._tile_size)

        self._sprite_sheet['door'] = sprite_sheet.image_at(door, self._colorkey)
        self._sprite_sheet['wall'] = sprite_sheet.image_at(wall, self._colorkey)
        self._sprite_sheet['floor'] = sprite_sheet.image_at(floor, self._colorkey)


    def _build(self):
        map_str = self.__map()
        y = 0
        for line in map_str:
            x = 0
            for col in line:
                if col == ' ':
                    self._tiles.append(floor.Floor(x, y, self._tile_size, self._sprite_sheet['floor']))
                elif col == '#':
                    self._tiles.append(wall.Wall(x, y, self._tile_size, self._sprite_sheet['wall']))
                elif col == 'D':
                    self._tiles.append(door.Door(x, y, self._tile_size, self._sprite_sheet['door']))
                else:
                    raise Exception("Tile is not recognised")
                x += 1
            y += 1

    def tile_iterator(self):
        for tile in self._tiles:
            yield tile

    def __map(self):
        """
        Represents the map as a matrix and should not be used outside this class (might change)
        :return:
        """
        return [
            "        #        ",
            "       #D#       ",
            "      #   #      ",
            "     #     #     ",
            "    #       #    ",
            "   #         #   ",
            "  #           #  ",
            " #             # ",
            "#D      D      D#",
            " #             # ",
            "  #           #  ",
            "   #         #   ",
            "    #       #    ",
            "     #     #     ",
            "      #   #      ",
            "       #D#       ",
            "        #        ",
            ]



