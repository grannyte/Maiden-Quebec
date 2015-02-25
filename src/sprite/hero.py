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
        self.sprite_sheet = Spritesheet(join(img, 'spritesheets', 'male.png'))
        self.actions = dict()
        self.actions['standing'] = {
            'north': self.sprite_sheet.image_at(pygame.Rect(0, 2 * 64, 64, 64), (0, 0, 0)),
            'west': self.sprite_sheet.image_at(pygame.Rect(0, 2 * 64, 64, 64), (0, 0, 0)),
            'south': self.sprite_sheet.image_at(pygame.Rect(0, 2 * 64, 64, 64), (0, 0, 0)),
            'east': self.sprite_sheet.image_at(pygame.Rect(0, 2 * 64, 64, 64), (0, 0, 0)),
        }
        self.actions['walking'] = {
            'north': self.sprite_sheet.image_at(pygame.Rect(0, 8 * 64, 64, 64), (0, 0, 0)),
            'west': self.sprite_sheet.image_at(pygame.Rect(0, 9 * 64, 64, 64), (0, 0, 0)),
            'south': self.sprite_sheet.image_at(pygame.Rect(0, 10 * 64, 64, 64), (0, 0, 0)),
            'east': self.sprite_sheet.image_at(pygame.Rect(0, 11 * 64, 64, 64), (0, 0, 0)),
        }
        self.actions['attacking'] = {
            'north': self.sprite_sheet.image_at(pygame.Rect(4 * 64, 12 * 64, 64, 64), (0, 0, 0)),
            'west': self.sprite_sheet.image_at(pygame.Rect(4 * 64, 13 * 64, 64, 64), (0, 0, 0)),
            'south': self.sprite_sheet.image_at(pygame.Rect(4 * 64, 14 * 64, 64, 64), (0, 0, 0)),
            'east': self.sprite_sheet.image_at(pygame.Rect(4 * 64, 15 * 64, 64, 64), (0, 0, 0)),
        }
        # Control
        self.action = 'standing'
        self.facing = 'south'
        self.image = self.actions[self.action][self.facing]

    def update(self, entities, blocks):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_UP] or key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_RIGHT]:
            self.action = 'walking'
            last_x, last_y = self.rect.left, self.rect.top
            if key_pressed[pygame.K_UP]:
                self.rect.top -= 1
                self.facing = 'north'
            elif key_pressed[pygame.K_DOWN]:
                self.rect.top += 1
                self.facing = 'south'
            elif key_pressed[pygame.K_LEFT]:
                self.rect.left -= 1
                self.facing = 'west'
            elif key_pressed[pygame.K_RIGHT]:
                self.rect.left += 1
                self.facing = 'east'
            collision_rect = self.__collide_rect()
            collisions = blocks.which_collide_with(collision_rect)
            if len(collisions) > 0:
                self.rect.left, self.rect.top = last_x, last_y
            self.image = self.actions[self.action][self.facing]
        elif key_pressed[pygame.K_z]:
            # Attack
            self.action = "attacking"
            self.image = self.actions[self.action][self.facing]


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