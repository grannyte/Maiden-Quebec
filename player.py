# -*- coding: utf-8 -*-
import os
import spritesheet
import pygame
from pygame import *
from entity import Entity


class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self._init_project_dir()
        self._init_spritesheet()
        rect = (0, 18*32, 32, 32)
        self.image = self._spritesheet.image_at(rect)
        self.image.set_colorkey((0, 0, 0))
        self.rect = Rect(x, y, 32, 32)
        self.heading = pygame.math.Vector2(0, 0)

    def _init_project_dir(self):
        """Initialize project directory"""
        full_path = os.path.realpath(__file__)
        self._project_dir = os.path.dirname(full_path)

    def _init_spritesheet(self):
        """Initialize spritesheet"""
        spritesheets = ["fantasy-tileset.png"]
        ss_path = os.path.join('', *[self._project_dir, 'data', spritesheets[0]])
        self._spritesheet = spritesheet.Spritesheet(ss_path)

    def update(self, platforms):
        self.rect.left += self.heading.x
        self.rect.top += self.heading.y
        self.collide(self.heading.x, self.heading.y, platforms)
        if self.rect.left % 32 == 0:
            self.heading.x = 0
        if self.rect.top % 32 == 0:
            self.heading.y = 0

    def control(self, local_event):
        if local_event.type == pygame.KEYDOWN:
            if local_event.key == pygame.K_LEFT:
                self.heading.x -= 4
            elif local_event.key == pygame.K_RIGHT:
                self.heading.x += 4
            elif local_event.key == pygame.K_UP:
                self.heading.y -= 4
            elif local_event.key == pygame.K_DOWN:
                self.heading.y += 4

# Collision TRES temporaire jusqu'a l'implementation de l'octree ou autre

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                p.collide(self, xvel, yvel)