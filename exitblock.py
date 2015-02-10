# -*- coding: utf-8 -*-
import pygame
from pygame import *
from tile import Tile


class ExitBlock(Tile):
    def __init__(self, x, y, spritesheet):
        Tile.__init__(self, x, y, spritesheet)
        rect = (1 * 64, 1 * 64, 64, 64)
        self.image = self._spritesheet.image_at(rect)

    def collide(self, p, xvel, yvel):
        pygame.event.post(pygame.event.Event(QUIT))