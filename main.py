# -*- coding: utf-8 -*-

import os
import pygame
import spritesheet

class Game:
    """Instantiates all the basic elements of the game."""

    def __init__(self, width=640, height=480):
        """Constructs the class"""
        """Instantiates pygame"""
        pygame.init()
        pygame.display.set_caption("prototype")
        self._init_screen(width, height)
        self._init_project_dir()
        self._init_spritesheet()

    def _init_screen(self, width, height):
        """Initialize pygame's screen"""
        self._width = width
        self._height = height
        self._screen = pygame.display.set_mode((width, height))

    def _init_project_dir(self):
        """Initialize project directory"""
        full_path = os.path.realpath(__file__)
        self._project_dir = os.path.dirname(full_path)

    def _init_spritesheet(self):
        """Initialize spritesheet"""
        spritesheets = ["fantasy-tileset.png"]
        ss_path = os.path.join('', *[self._project_dir, 'data', spritesheets[0]])
        self._spritesheet = spritesheet.Spritesheet(ss_path)

    def _load_hero(self, x, y):
        hero = self._spritesheet.image_at((0, 18*32, 32, 32))
        self._screen.blit(hero, (x, y))

    def run(self):
        """Main loop of the game"""
        colors = {'white': (255, 255, 255)}
        clock = pygame.time.Clock()
        is_running = True
        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
            self._screen.fill(colors['white'])
            self._load_hero(0, 0)
            pygame.display.update()
            clock.tick(60)
        pygame.quit()
        quit()

if __name__ == "__main__":
    if not pygame.font:
        print('Warning, fonts disabled')
    if not pygame.mixer:
        print('Warning, sound disabled')
    if __name__ == "__main__":
        game = Game()
        game.run()