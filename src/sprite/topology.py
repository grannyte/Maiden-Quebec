__author__ = 'plperron'

import pygame
import config
from os.path import join
from config import tile
from src.sprite.spritesheet import Spritesheet

def build_temple():
    zone = [
        '###################',
        '#         ##### # #',
        '#              D# #',
        '#         ##### # #',
        '#              D# #',
        '#         ##### # #',
        '#              D# #',
        '#         #####   #',
        '###################',
    ]
    topology = dict()
    topology['zone'] = zone
    topology['height'] = len(zone)
    topology['width'] = len(zone[0])
    tile_size = 64
    topology['tile_size'] = tile_size
    temple = Spritesheet(join(tile, 'temple', 'wall.png'))
    topology['wall'] = '#'
    topology['wall_sprite'] = temple.image_at(pygame.Rect(0, 0, 64, 64), (0, 0, 0))
    topology['walls'] = __build_wall_sprite(zone, '#', tile_size)
    topology['door'] = 'D'
    temple = Spritesheet(join(tile, 'temple', 'door.png'))
    topology['door_sprite'] = temple.image_at(pygame.Rect(0, 0, 64, 64), (0, 0, 0))
    topology['doors'] = __build_wall_sprite(zone, 'D', tile_size)
    topology['floor'] = ' '
    temple = Spritesheet(join(tile, 'temple', 'floor.png'))
    topology['floor_sprite'] = temple.image_at(pygame.Rect(0, 0, 64, 64), (0, 0, 0))
    topology['floors'] = __build_wall_sprite(zone, ' ', tile_size)
    return topology



def __build_wall_sprite(zone, symbol, tile_size):
    return [pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
            for y in range(0, len(zone))
            for x in range(0, len(zone[y]))
            if(zone[y][x] == symbol)]
