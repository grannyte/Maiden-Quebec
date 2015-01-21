# -*- coding: utf-8 -*-

import pygame
from pygame import *
from entity import Entity


class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = Surface((32, 32))
        self.image.fill(Color("#0000FF"))
        self.image.convert()
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass

    def control(self, local_event):
        if local_event.type == pygame.KEYDOWN:
            if local_event.key == pygame.K_LEFT:
                self.rect.left -= 32
            elif local_event.key == pygame.K_RIGHT:
                self.rect.left += 32
            elif local_event.key == pygame.K_UP:
                self.rect.top -= 32
            elif local_event.key == pygame.K_DOWN:
                self.rect.top += 32