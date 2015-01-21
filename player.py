# -*- coding: utf-8 -*-
import os
import spritesheet
import pygame
from pygame import *
from entity import Entity
import exitblock
import Spike


class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self._init_project_dir()
        self._init_spritesheet()
        rect = (0, 18*32, 32, 32)
        self.image = self._spritesheet.image_at(rect)
        self.rect = Rect(x, y, 32, 32)

    def _init_project_dir(self):
        """Initialize project directory"""
        full_path = os.path.realpath(__file__)
        self._project_dir = os.path.dirname(full_path)

    def _init_spritesheet(self):
        """Initialize spritesheet"""
        spritesheets = ["fantasy-tileset.png"]
        ss_path = os.path.join('', *[self._project_dir, 'data', spritesheets[0]])
        self._spritesheet = spritesheet.Spritesheet(ss_path)

    def update(self):
        pass

    def control(self, local_event, platforms):
        if local_event.type == pygame.KEYDOWN:
            if local_event.key == pygame.K_LEFT:
                self.rect.left -= 32
                self.collide(-32, 0, platforms)
            elif local_event.key == pygame.K_RIGHT:
                self.rect.left += 32
                self.collide(32, 0, platforms)
            elif local_event.key == pygame.K_UP:
                self.rect.top -= 32
                self.collide(0, -32, platforms)
            elif local_event.key == pygame.K_DOWN:
                self.rect.top += 32
                self.collide(0, 32, platforms)

# Collision TRES temporaire jusqu'a l'implementation de l'octree ou autre

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, exitblock.ExitBlock):
                    pygame.event.post(pygame.event.Event(QUIT))
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                if isinstance(p, Spike.Spike):
                    if xvel > 0:
                        self.rect.right = (p.rect.left-32)
                    if xvel < 0:
                        self.rect.left = (p.rect.right+32)
                    if yvel > 0:
                        self.rect.bottom = (p.rect.top-32)
                    if yvel < 0:
                        self.rect.top = (p.rect.bottom+32)