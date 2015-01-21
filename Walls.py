__author__ = 'granyte'




import spritesheet
import os
import pygame
from pygame import *
from tile import Tile


class Walls(Tile):
    def __init__(self, x, y):
        Tile.__init__(self, x, y)
        rect = (1*32, 2*32, 32, 32)
        self.image = self._spritesheet.image_at(rect)

    def collide(self, p, xvel, yvel):
        if xvel > 0:
            p.rect.right = self.rect.left
        if xvel < 0:
            p.rect.left = self.rect.right
        if yvel > 0:
            p.rect.bottom = self.rect.top
        if yvel < 0:
            p.rect.top = self.rect.bottom


