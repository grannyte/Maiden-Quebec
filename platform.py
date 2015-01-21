# -*- coding: utf-8 -*-
import os
import spritesheet
import pygame
from pygame import *
from entity import Entity



class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self._init_project_dir()
        self._init_spritesheet()
        rect = (32, 2*32, 32, 32)
        self.image = self._spritesheet.image_at(rect)
        self.rect = Rect(x, y, 32, 32)

    def _init_project_dir(self):
        """Initialize project directory"""
        full_path = os.path.realpath(__file__)
        self._project_dir = os.path.dirname(full_path)

    def _init_spritesheet(self):
        """Initialize spritesheet"""
        spritesheets = ["fantasy-tileset.png"]
        ss_path = os.path.join('', *[self._project_dir, 'data', spritesheets[0]])
        self._spritesheet = spritesheet.Spritesheet(ss_path)

    def update(self):
        pass

    def collide(self, p, xvel, yvel):
        if xvel > 0:
            p.rect.right = self.rect.left
        if xvel < 0:
            p.rect.left = self.rect.right
        if yvel > 0:
            p.rect.bottom = self.rect.top
        if yvel < 0:
            p.rect.top = self.rect.bottom