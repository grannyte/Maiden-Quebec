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

    def collide(self, p, xvel, yvel):
        pygame.event.post(pygame.event.Event(QUIT))