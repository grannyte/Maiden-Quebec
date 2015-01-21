# -*- coding: utf-8 -*-
import spritesheet
import os
import pygame
from pygame import *
from tile import Tile


class ExitBlock(Tile):
    def __init__(self, x, y):
        Tile.__init__(self, x, y)
        rect = (32*6, 2*32, 32, 32)
        self.image = self._spritesheet.image_at(rect)

    def collide(self, p, xvel, yvel):
        pygame.event.post(pygame.event.Event(QUIT))