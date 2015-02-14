# -*- coding: utf-8 -*-
from __future__ import print_function

import pygame

class StatusHud(object):
    def __init__(self):
        self.hud_font = pygame.font.SysFont("monospace", 16)
        self.hud_font.set_bold(True)

    def get_label(self):
        pass

    def get_content(self):
        pass