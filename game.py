# -*- coding: utf-8 -*-
from __future__ import print_function

import pygame
from pygame import *

from src.camera import ComplexCamera
from src.hud.hud_health import HudHealth
from src.sprite.hero import Hero
from src.map.temple import Temple
from client import Client

from os.path import realpath, dirname


class Game():
    """
    Run the game with local resource and get extra from server (players, monsters, drops, quests)
    """
    def __init__(self, project_directory):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        self.project_directory = project_directory
        self.timer = time.Clock()
        # self.screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN | pygame.HWSURFACE)
        self.screen = display.set_mode((800, 600), pygame.HWSURFACE)
        self.camera = ComplexCamera(1024, 768, 800, 600)
        self._hud_health = HudHealth()

        # TODO: Client should get updates from server
        self.player = Hero(8, 8, 64, project_directory)
        self.entities = sprite.Group()
        self.entities.add(self.player)

        self.location = Temple(project_directory)
        self.sprites = sprite.Group()
        for tile in self.location.tiles_iterator():
            self.sprites.add(tile)
        self.blocks = sprite.Group()
        for block in self.location.blocks_iterator():
            self.blocks.add(block)


    def run(self):
        fps = 60
        is_running = True
        while is_running:
            self.timer.tick(fps)
            for e in pygame.event.get():
                if e.type == QUIT:
                    is_running = False
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    is_running = False

            if pygame.key.get_focused():
                pressed = pygame.key.get_pressed()
                self.player.control(pressed)

            # TODO: AI

            self._update()
            self._draw()

    def _update(self):
        self.entities.update(self.blocks)
        self.sprites.update()
        self.camera.update(self.player)

    def _draw(self):
        for s in self.sprites:
            self.screen.blit(s.image, self.camera.apply(s))

        for e in self.entities:
            self.screen.blit(e.image, self.camera.apply(e))

        hh = self._hud_health.update(8, 32)
        self.screen.blit(hh['label'], hh['at'])
        pygame.draw.rect(self.screen, hh['color'], hh['hp'])

        pygame.display.update()


def _init_project_directory():
        """
        Initializes project's root directory
        """
        full_path = realpath(__file__)
        return dirname(full_path)


if __name__ == '__main__':
    project_directory = _init_project_directory()
    game = Game(project_directory)
    game.run()