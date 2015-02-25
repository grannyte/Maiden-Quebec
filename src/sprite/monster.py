# -*- coding: utf-8 -*-
from __future__ import print_function

import pygame

from os.path import join
from config import img
from src.sprite.spritesheet import Spritesheet
import random

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
        self.direction = 'up'
        self.direction_count = 0
        self.random = random.randrange(1,5)*64

    def update(self, quad):
        if(self.direction == 'up'):
            self.rect.top -= 1
            collision_rect = self.__collide_rect()
            collisions = quad.which_collide_with(collision_rect)
            if len(collisions) > 0 or self.direction_count > self.random*64:
                self.random = random.randrange(1,5)
                self.direction = 'left'
                self.direction_count = 0
        elif(self.direction == 'left'):
            self.rect.left -= 1
            collision_rect = self.__collide_rect()
            collisions = quad.which_collide_with(collision_rect)
            if len(collisions) > 0 or self.direction_count > self.random*64:
                self.random = random.randrange(1,5)
                self.direction = 'down'
                self.direction_count = 0
        elif(self.direction == 'down'):
            self.rect.top += 1
            collision_rect = self.__collide_rect()
            collisions = quad.which_collide_with(collision_rect)
            if len(collisions) > 0 or self.direction_count > self.random*64:
                self.random = random.randrange(1,5)
                self.direction = 'right'
                self.direction_count = 0
        else:
            self.rect.left += 1
            collision_rect = self.__collide_rect()
            collisions = quad.which_collide_with(collision_rect)
            if len(collisions) > 0 or self.direction_count > self.random*64:
                self.random = random.randrange(1,5)
                self.direction = 'up'
                self.direction_count = 0
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