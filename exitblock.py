# -*- coding: utf-8 -*-
import spritesheet
import os
import pygame
from pygame import *
from platform import Platform


class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        rect = (32*6, 2*32, 32, 32)
        self.image = self._spritesheet.image_at(rect)

    def _init_project_dir(self):
        """Initialize project directory"""
        full_path = os.path.realpath(__file__)
        self._project_dir = os.path.dirname(full_path)

    def _init_spritesheet(self):
        """Initialize spritesheet"""
        spritesheets = ["fantasy-tileset.png"]
        ss_path = os.path.join('', *[self._project_dir, 'data', spritesheets[0]])
        self._spritesheet = spritesheet.Spritesheet(ss_path)

