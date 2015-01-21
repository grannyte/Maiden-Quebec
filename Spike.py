__author__ = 'granyte'



import spritesheet
import pygame
from pygame import *
from entity import Entity
from platform import Platform




class Spike(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        rect = (3*32, 3*32, 32, 32)
        self.image = self._spritesheet.image_at(rect)

    def collide(self, p, xvel, yvel):
        if xvel > 0:
            p.rect.right = (self.rect.left-32)
        if xvel < 0:
            p.rect.left = (self.rect.right+32)
        if yvel > 0:
            p.rect.bottom = (self.rect.top-32)
        if yvel < 0:
            p.rect.top = (self.rect.bottom+32)