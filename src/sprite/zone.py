__author__ = 'plperron'

import pygame

class Zone():
    def  __init__(self, topology):
        self.height = topology.height
        self.width = topology.width
        self.sprite_sheet = topology.sprite_sheet
        self.wall_symbol = topology.wall_symbol
        self.door_symbol = topology.door_symbol
        self.floor_symbol = topology.floor_symbol

    def build(self):
        pass