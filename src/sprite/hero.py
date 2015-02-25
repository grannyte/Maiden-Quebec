# -*- coding: utf-8 -*-
from __future__ import print_function

import pygame

from src.sprite.spritesheet import Spritesheet

class Hero(pygame.sprite.Sprite):

    def __init__(self, player_infos):
        """
        :param player_infos: A dict with the following keys
            user,password,skin,level,cur_hp,max_hp,
            strength,endurance,dexterity,intelligence,wisdom,
            zone,coord_x,coord_y,
            left_hand,right_hand,armor
        :return:
        """
        pygame.sprite.Sprite.__init__(self)
        self.player_infos = player_infos
        self.rect = player_infos['rect']
        sprite_sheet = Spritesheet("/home/plperron/PycharmProjects/Maiden-Quebec/data/img/spritesheets/male.png")
        self.image = sprite_sheet.image_at(pygame.Rect(0, 0, 64, 64))

    def control(self, key_pressed):
        print("bob")
        pass