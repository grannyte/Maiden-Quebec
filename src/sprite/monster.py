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
        self.sprite_sheet = Spritesheet(join(img, 'spritesheets', 'male.png'))
        self.image = self.sprite_sheet.image_at(pygame.Rect(0, 2 * 64, 64, 64), (0, 0, 0))
        # Control
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
        self.move = 0
        self.action = 'standing'
        self.facing = 'south'
        self.image = self.actions[self.action][self.facing]

    def update(self, quad):
        """
        Tries to attack the player in the first place, he wanders around otherwise
        :param quad:
        :return:
        """
        if self.is_enemy_seen():
            pass
        elif self.move > 0:  # keep moving in the same direction
            last_left, last_top, last_facing = self.rect.left, self.rect.top, self.facing
            if self.facing == 'north':
                self.rect.top -= 1
            elif self.facing == 'south':
                self.rect.top += 1
            elif self.facing == 'west':
                self.rect.left -= 1
            elif self.facing == 'east':
                self.rect.left += 1
            self.move -= 1
            collision_rect = self.__collide_rect()
            collisions = quad.which_collide_with(collision_rect)
            if len(collisions) > 0:
                self.rect.left, self.rect.top, self.facing = last_left, last_top, last_facing
        else:  # Otherwise he wanders around
            directions = ['north', 'south', 'west', 'east']
            rand = random.randint(0, len(directions) * 128 - 1)
            if rand % 128 == 0:
                rand = int(rand / 128)
                self.facing = directions[rand]
                self.move = 64




    def is_enemy_seen(self):
        return False

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