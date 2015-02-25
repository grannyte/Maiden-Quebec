# -*- coding: utf-8 -*-
from __future__ import print_function

from pygame import K_RIGHT, K_LEFT, K_UP, K_DOWN

from os.path import join

from src.sprite.life_form import LifeForm


class Hero(LifeForm):
    def __init__(self, player_infos):
        """
        :param player_infos: A dict with the following keys
            user,password,skin,level,cur_hp,max_hp,
            strength,endurance,dexterity,intelligence,wisdom,
            zone,coord_x,coord_y,
            left_hand,right_hand,armor
        :return:
        """
        self.playerinfos = player_infos
        pass



    def _change_appearance(self, spritesheet_path, tile_size):
        LifeForm._change_appearance(self, spritesheet_path, tile_size)