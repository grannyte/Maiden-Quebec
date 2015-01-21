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
