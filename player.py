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
        self.rect.left += 32
        self.rect.top += 32