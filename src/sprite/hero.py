# -*- coding: utf-8 -*-
from __future__ import print_function

from pygame import K_RIGHT, K_LEFT, K_UP, K_DOWN

from os.path import join

from src.sprite.life_form import LifeForm


class Hero(LifeForm):
    def __init__(self, x, y, tile_size, project_dir):
        LifeForm.__init__(self, x, y, tile_size, join(project_dir, 'data', 'img', 'rogue.png'))
        self.last_x, self.last_y = self.new_x, self.new_y = self.rect.left, self.rect.top
        self.is_walking = False
        self.is_collision_checked = False
        self._action = 'walk'
        self._heading = '_south'
        self.frame = 2
        self.speed = 2 # in frame rate
        self.image = self._sprite_sheet[self._action + self._heading][self.frame]

    def control(self, key_pressed):
        """
        Uses keyboard input to dictate the next character behavior
        :param key_pressed: A bit list representing whether or not the ascii key(index) is pressed
        :return:
        """
        if self.is_walking:
            return
        if key_pressed[K_UP]:
            self.walk(self.rect.left, self.rect.top - self.tile_size, '_north')
        elif key_pressed[K_DOWN]:
            self.walk(self.rect.left, self.rect.top + self.tile_size, '_south')
        elif key_pressed[K_RIGHT]:
            self.walk(self.rect.left + self.tile_size, self.rect.top, '_east')
        elif key_pressed[K_LEFT]:
            self.walk(self.rect.left - self.tile_size, self.rect.top, '_west')

    def walk(self, x, y, heading):
        self.new_x = self.rect.left = x
        self.new_y = self.rect.top = y
        self._action = 'walk'
        self._heading = heading
        self.is_walking = True
        self.frame = 0

    # TODO: Refactoring (decorator pattern multiple class action ?)
    def update(self, blocks):
        self._update_walking(blocks)

    def _update_walking(self, blocks):
        if not self.is_walking:
            return
        if not self.is_collision_checked:
            if self.will_collide(blocks):
                self.rect.left, self.rect.top = self.last_x, self.last_y
                self.is_walking = False
                return
            self.rect.left, self.rect.top = self.last_x, self.last_y
            self.is_collision_checked = True
        if self.speed > 0:
            self.speed -= 1
            return
        self.speed = 3
        # action + no collision
        # Update currently location
        self.rect.left = self.last_x + ((self.new_x - self.last_x) / len(self._sprite_sheet) * self.frame * self.speed)
        print(self.rect.left)
        self.rect.top = self.last_y + ((self.new_y - self.last_y) / len(self._sprite_sheet) * self.frame * self.speed)
        self.image = self._sprite_sheet[self._action + self._heading][self.frame]
        self.frame += 1
        # Cycle
        if self.frame == len(self._sprite_sheet[self._action + self._heading]):
            self.is_walking = False
            self.is_collision_checked = False
            self.frame = 0
            self.last_x, self.last_y = self.rect.left, self.rect.top = self.new_x, self.new_y

    def will_collide(self, blocks):
        """
        Determines whether or not the hero new position will collide with something.
        :param blocks: Tiles that may collide with.
        :return: True if any(blocks).rect == self.rect else False
        """
        for block in blocks:
            if block.rect.left != self.rect.left:
                continue
            if block.rect.top != self.rect.top:
                continue
            return True
        return False

    def _change_appearance(self, spritesheet_path, tile_size):
        LifeForm._change_appearance(self, spritesheet_path, tile_size)