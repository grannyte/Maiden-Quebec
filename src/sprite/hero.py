# -*- coding: utf-8 -*-
from __future__ import print_function

import pygame

from os.path import join
from config import img
from src.sprite.spritesheet import Spritesheet

class Hero(pygame.sprite.Sprite):

    def __init__(self, hero_infos):
        """
        :param player_infos: A dict with the following keys
            user,password,skin,level,cur_hp,max_hp,
            strength,endurance,dexterity,intelligence,wisdom,
            zone,coord_x,coord_y,
            left_hand,right_hand,armor
        :return:
        """
        pygame.sprite.Sprite.__init__(self)
        self.hero_infos = hero_infos
        self.rect = hero_infos['rect']
        self.tile_size = hero_infos['tile_size']
        sprite_sheet = Spritesheet(join(img, 'spritesheets', 'male.png'))
        self.image = sprite_sheet.image_at(pygame.Rect(0, 2 * 64, 64, 64), (0, 0, 0))
        # Control
        self.isStandingStill = True


    def control(self, key_pressed, quad):
        last_x, last_y = self.rect.left, self.rect.top
        if key_pressed[pygame.K_UP]:
            self.rect.top -= 1
        elif key_pressed[pygame.K_DOWN]:
            self.rect.top += 1
        elif key_pressed[pygame.K_LEFT]:
            self.rect.left -= 1
        elif key_pressed[pygame.K_RIGHT]:
            self.rect.left += 1
        collision_rect = self.__collide_rect()
        collisions = quad.which_collide_with(collision_rect)
        if len(collisions) > 0:
            self.rect.left, self.rect.top = last_x, last_y
            print("COLLISION")
            print(self.rect)
            print(collision_rect)
            for collision in collisions:
                print(collision.rect, collision.rect)

    def update(self):
        pass


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