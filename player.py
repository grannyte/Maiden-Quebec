# -*- coding: utf-8 -*-
import pygame
from pygame import *

from character import Character


class Player(Character):
    def __init__(self, x, y, spritesheet):
        Character.__init__(self, x, y, spritesheet)

    def control(self, pressed, since_last_tick):
        self.ticks += since_last_tick
        self._heading.x = 0
        self._heading.y = 0
        actual_action = ''
        if self.ticks >= 1000.0 / len(self._animations):
            if pressed[pygame.K_LEFT]:
                self._action = 'walk'
                self._facing = '_west'
                actual_action = self._action + self._facing
                self._animations = self._spritesheet[actual_action]
                self._heading.x = -64 / len(self._animations)
                self._is_standing_still = False
            elif pressed[pygame.K_RIGHT]:
                self._action = 'walk'
                self._facing = '_est'
                actual_action = self._action + self._facing
                self._animations = self._spritesheet[actual_action]
                self._heading.x = 64 / len(self._animations)
                self._is_standing_still = False
            elif pressed[pygame.K_UP]:
                self._action = 'walk'
                self._facing = '_north'
                actual_action = self._action + self._facing
                self._animations = self._spritesheet[actual_action]
                self._heading.y = -64 / len(self._animations)
                self._is_standing_still = False
            elif pressed[pygame.K_DOWN]:
                self._action = 'walk'
                self._facing = '_south'
                actual_action = self._action + self._facing
                self._animations = self._spritesheet[actual_action]
                self._heading.y = 64 / len(self._animations)
                self._is_standing_still = False
            elif pressed[pygame.K_z]:
                self._action = 'attack'
                actual_action = self._action + self._facing
                self._animations = self._spritesheet[actual_action]
                self._is_standing_still = False
            elif pressed[pygame.K_s]:
                self._is_standing_still = True
                pass  # TODO: status HUD
            elif pressed[pygame.K_i]:
                self._is_standing_still = True
                pass  # TODO: inventory HUD
            else:
                self._is_standing_still = True
            self.ticks = 0
        if actual_action != self._last_action:
            self._last_action = actual_action
            Character._frame = 0
