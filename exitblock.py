# -*- coding: utf-8 -*-

import pygame
from pygame import *
from platform import Platform


class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image.fill(Color("#0033FF"))