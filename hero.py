# -*- coding: utf-8 -*-

import pygame


class Hero(pygame.sprite.Sprite):

    def __init__(self, spritesheet, group):
        pygame.sprite.Sprite.__init__(self, group)
        rect = (0, 18*32, 32, 32)
        self.image = spritesheet.image_at(rect)
        self.rect = (100, 100) #  sprite pos on the screen
        self.radius = 16  # collide check

    def update(self):
       self.rect.center = self.pos

    def control(self, event):
        x, y = self.rect
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 32
            elif event.key == pygame.K_RIGHT:
                x += 32
            elif event.key == pygame.K_UP:
                y -= 32
            elif event.key == pygame.K_DOWN:
                y += 32
        self.rect = (x, y)