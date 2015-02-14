# -*- coding: utf-8 -*-
from __future__ import print_function

from pygame import K_RIGHT

from os.path import join

from src.sprite.life_form import LifeForm


class Hero(LifeForm):
    def __init__(self, x, y, tile_size, project_dir):
        LifeForm.__init__(self, x, y, tile_size, join(project_dir, 'data', 'img', 'rogue.png'))

    def control(self, key_pressed):
        """
        Uses keyboard input to dictate the next character behavior
        :param key_pressed: A bit list representing whether or not the ascii key(index) is pressed
        :return:
        """
        if key_pressed[K_RIGHT]:
            print("going right")

    def update(self, *args):
        pass
        #self.rect.left += 1


    def _change_appearance(self, spritesheet_path, tile_size):
        LifeForm._change_appearance(self, spritesheet_path, tile_size)