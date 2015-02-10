# -*- coding: utf-8 -*-

import pygame


class Hero(pygame.sprite.Sprite):

    def __init__(self, spritesheet, group):
        pygame.sprite.Sprite.__init__(self, group)
        rect = (0, 0, 64, 64)
        self.image = spritesheet.image_at(rect)
        self.rect = (256, 256) #  sprite pos on the screen
        self.radius = 16  # collide check

    def update(self):
        self.rect.center = self.pos

    def control(self, event):
        x, y = self.rect
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 64
            elif event.key == pygame.K_RIGHT:
                x += 64
            elif event.key == pygame.K_UP:
                y -= 64
            elif event.key == pygame.K_DOWN:
                y += 64
        self.rect = (x, y)