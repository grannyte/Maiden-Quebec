# -*- coding: utf-8 -*-
import os
import spritesheet
import pygame
from pygame import *
from entity import Entity


class Player(Entity):
    def __init__(self, x, y, spritesheet):
        Entity.__init__(self)
        #Hero's spritesheet must have the same pattern.  see rogue.png as an example
        self._spritesheet = spritesheet
        rect = (0, 0, 64, 64)
        self.image = self._spritesheet.image_at(rect)
        self.image.set_colorkey((0, 0, 0))
        self.rect = Rect(x, y, 64, 64)
        self.heading = pygame.math.Vector2(0, 0)

    def update(self, platforms):
        self.rect.left += self.heading.x
        self.rect.top += self.heading.y
        self.collide(self.heading.x, self.heading.y, platforms)
        if self.rect.left % 64 == 0:
            self.heading.x = 0
        if self.rect.top % 64 == 0:
            self.heading.y = 0

    def control(self, pressed):
        if pressed[pygame.K_LEFT]:
            self.heading.x -= 4
        elif pressed[pygame.K_RIGHT]:
            self.heading.x += 4
        elif pressed[pygame.K_UP]:
            self.heading.y -= 4
        elif pressed[pygame.K_DOWN]:
            self.heading.y += 4
        elif pressed[pygame.K_s]:
            self.heading.y += 4  # TODO: status HUD
        elif pressed[pygame.K_i]:
            self.heading.y += 4  # TODO: inventory HUD

# Collision TRES temporaire jusqu'a l'implementation de l'octree ou autre

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                p.collide(self, xvel, yvel)