# -*- coding: utf-8 -*-
from __future__ import print_function

# TODO: --user pl --password lp --host localhost --port 9090

import argparse
import re

import pygame
from pygame import *
from src.camera import ComplexCamera
from src.hud.hud_health import HudHealth

from src.map import Map
from src.network.client import Client
from config import init_project_directory


#  TODO: ???Singleton or convention??? remove the class and put everything at module level
class Game():
    """
    Run the game with local resource and get extras from server (players, monsters, drops, quests)
    """
    def __init__(self, client, user):
        self.client = client

        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        self.project_directory = init_project_directory()
        self.timer = time.Clock()
        # self.screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN | pygame.HWSURFACE)
        self.screen = display.set_mode((800, 600), pygame.HWSURFACE)

        # TODO: New/Load Game HUD



        self.player = Hero(client.who_is(user))
        self.dongeon = Map(client.where_is(user))
        # Those are updated by the server
        self.entities = sprite.Group()
        self.sprites = sprite.Group()
        self.blocks = sprite.Group()

        # self.screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN | pygame.HWSURFACE)
        self.screen = display.set_mode((800, 600), pygame.HWSURFACE)
        self.camera = ComplexCamera(2048, 2048, 800, 600)
        self._hud_health = HudHealth()


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

            self.client.where_is(self.user)
            self._update()
            self._draw()

    def _update(self):
        # TODO s:
        # Do the player know who he is


        # Does the player know where he is ?


        # Does he know what the others are

        # Does he know what he looks like

        # Does he know what the others look like


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

def parser_args():
    parser = argparse.ArgumentParser(prog="maid", description="MaindenQuebec's client")
    parser.add_argument('--user', type=str, required=True, help="Player's user name")
    parser.add_argument('--password', type=str, required=True, help="Player's password")
    parser.add_argument('--host', type=str, required=True, help="Server's hostname")
    parser.add_argument('--port', type=int, required=True, help="Server's listening port")
    args =  parser.parse_args()
    # TODO: Add others regex
    if len(re.match(r'\w{1,16}', args.user).group(0)) != len(args.user):
        raise Exception("User name must have between 1 and 16 (inclusive) character from A to Z, a to z, 0 to 9 and _")
    return args.user, args.password, args.host, args.port


if __name__ == '__main__':
    args = parser_args()
    user, _, _, _ = args
    client = Client(args)
    game = Game(client, user)
    game.run()

__author__ = "plperron, jmjodoin, ddelisle"