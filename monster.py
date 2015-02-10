# -*- coding: utf-8 -*-
from character import Character


class Monster(Character):
    def __init__(self, x, y, spritesheet):
        Character.__init__(self, x, y, spritesheet)