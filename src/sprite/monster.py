# -*- coding: utf-8 -*-
from __future__ import print_function

import pygame

from os.path import join
from config import img
from src.sprite.spritesheet import Spritesheet

class Monster(pygame.sprite.Sprite):

    def __init__(self, monster_infos):
        """
        :param player_infos: A dict with the following keys
            user,password,skin,level,cur_hp,max_hp,
            strength,endurance,dexterity,intelligence,wisdom,
            zone,coord_x,coord_y,
            left_hand,right_hand,armor
        :return:
        """
        pygame.sprite.Sprite.__init__(self)
        self.hero_infos = monster_infos
        self.rect = monster_infos['rect']
        self.tile_size = monster_infos['tile_size']
        sprite_sheet = Spritesheet(join(img, 'spritesheets', 'red_ork.png'))
        self.image = sprite_sheet.image_at(pygame.Rect(0, 2 * 64, 64, 64), (0, 0, 0))
        # Control
        self.isStandingStill = True
        self.direction = 'left'
        self.direction_count = 0

    def update(self):
        if(self.direction == 'left'):
            self.rect.top -= 1
            if(self.direction_count == 64):
                self.direction_count = 0
                self.direction = 'up'
        elif(self.direction == 'up'):
            self.rect.left += 1
            if(self.direction_count == 64):
                self.direction_count = 0
                self.direction = 'right'
        elif(self.direction == 'right'):
            self.rect.top += 1
            if(self.direction_count == 64):
                self.direction_count = 0
                self.direction = 'down'
        else:
            self.rect.left -= 1
            if(self.direction_count == 64):
                self.direction_count = 0
                self.direction = 'left'
        self.direction_count += 1


    def __collide_rect(self):
        """
        Calculate a colliding box base on hero's rect.  The box starts at 1/4 left/top and ends at 3/4
        :return:
        """
        buffer = self.tile_size / 4
        size = self.tile_size / 2
        collide_left = self.rect.left + buffer
        collide_top = self.rect.top + buffer
        return pygame.Rect(collide_left, collide_top, size, size)