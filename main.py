import pygame
import spritesheet
import os
from pygame import *
from player import Player
from tile import Tile
from exitblock import ExitBlock
from camera import ComplexCamera
from map import create_level
from map import LSystemMap
from map import Gene
from spike import Spike
from walls import Walls

WIN_WIDTH = 1920
WIN_HEIGHT = 1080
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30


class Game():
    def __init__(self):
        self._init_pygame()
        self._init_project_dir()
        self._init_spritesheet()
        self._init_game_variable()
        self._load_level()

        self.camera = ComplexCamera(self.total_level_width, self.total_level_height, WIN_WIDTH, WIN_HEIGHT)

        self.run(self.camera)

    def _init_project_dir(self):
        """Initialize project directory"""
        full_path = os.path.realpath(__file__)
        self._project_dir = os.path.dirname(full_path)

    def _init_spritesheet(self):
        """Initialize spritesheet"""
        spritesheets = ["fantasy-tileset.png"]
        ss_path = os.path.join('', *[self._project_dir, 'data', spritesheets[0]])
        self._spritesheet = spritesheet.Spritesheet(ss_path)

    def _init_game_variable(self):
        self.timer = pygame.time.Clock()
        self.map = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()
        self.player = Player(50*32, 50*32, self._spritesheet)
        self.platforms = []

    def _init_pygame(self):
        self.pygame = pygame
        self.pygame.init()
        self.screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
        self.pygame.display.set_caption("Use arrows to move!")
        self.bg = Surface((32, 32))
        self.bg.convert()
        self.bg.fill(Color("#000000"))

    def _load_level(self):
        x = y = 0
        local_map = LSystemMap(3, "{ATA>{ATEAS}}<A")

        local_map.append_gene(Gene("T", "TTT"))
        local_map.append_gene(Gene("A", ">{AT<}"))
        local_map.append_gene(Gene("TT", "[TA]T"))
        local_map.append_gene(Gene("AT", "(AT)"))
        local_map.append_gene(Gene("TA", "{TAS}"))
        local_map.append_gene(Gene("S", "{<TAS}"))
        local_map.append_gene(Gene("E", "{<TES}"))
        self.level = local_map.buildmap(100, 100)
            #create_level()
        # build the level
        for row in self.level:
            for col in row:
                if col == "P":
                    p = Walls(x, y, self._spritesheet)
                    self.platforms.append(p)
                    self.entities.add(p)
                elif col == "S":
                    p = Spike(x, y, self._spritesheet)
                    self.platforms.append(p)
                    self.entities.add(p)
                elif col == "E":
                    e = ExitBlock(x, y, self._spritesheet)
                    self.platforms.append(e)
                    self.entities.add(e)
                else:
                    p = Tile(x, y, self._spritesheet)
                    self.platforms.append(p)
                    self.map.add(p)
                x += 32
            y += 32
            x = 0
        self.total_level_width = len(self.level[0]) * 32
        self.total_level_height = len(self.level) * 32
        self.entities.add(self.player)

    def run(self, camera):
        is_running = True
        while is_running:
            self.timer.tick(60)

            for e in pygame.event.get():
                if e.type == QUIT:
                    raise SystemExit
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    raise SystemExit
                else:
                    self.player.control(e)

            # draw background
            for y in range(32):
                for x in range(32):
                    self.screen.blit(self.bg, (x * 32, y * 32))

            self.camera.update(self.player)

            # update player, draw everything else
            self.player.update(self.platforms)

            for t in self.map:
                self.screen.blit(t.image, camera.apply(t))

            for e in self.entities:
                self.screen.blit(e.image, camera.apply(e))

            self.pygame.display.update()





if __name__ == "__main__":
    game = Game()
    game.run()