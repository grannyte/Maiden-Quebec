import pygame
import spritesheet
import os
from pygame import *
from player import Player
from tile import Tile
from exitblock import ExitBlock
from camera import ComplexCamera
from map import create_level
from spike import Spike
from wall import Walls

WIN_WIDTH = 800
WIN_HEIGHT = 640
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
        spritesheets = {'rpg': 'wall.png', 'rogue': 'rogue.png'}
        ss_rpg = os.path.join('', *[self._project_dir, 'data', spritesheets['rpg']])
        self._ss_rpg = spritesheet.Spritesheet(ss_rpg)
        ss_rogue = os.path.join('', *[self._project_dir, 'data', spritesheets['rogue']])
        self._ss_rogue = spritesheet.Spritesheet(ss_rogue)

    def _init_music(self):
        musics = {'donjon': 'dark_theme.ogg'}
        donjon = os.path.join('', *[self._project_dir, 'data', musics['donjon']])
        pygame.mixer.music.load(donjon)
        pygame.mixer.music.play(-1)

    def _init_game_variable(self):
        self.timer = pygame.time.Clock()
        self.map = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()
        self.player = Player(64, 64, self._ss_rogue)
        self.platforms = []

    def _init_pygame(self):
        self.pygame = pygame
        self.pygame.mixer.pre_init(44100, -16, 2, 2048)
        self.pygame.init()
        self.screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
        self.pygame.display.set_caption("Maiden Quebec")
        self.bg = Surface((64, 64))
        self.bg.convert()
        self.bg.fill((0, 0, 0))

    def _load_level(self):
        x = y = 0
        self.level = create_level()
        # build the level
        for row in self.level:
            for col in row:
                if col == "P":
                    p = Walls(x, y, self._ss_rpg)
                    self.platforms.append(p)
                    self.entities.add(p)
                elif col == "S":
                    p = Spike(x, y, self._ss_rpg)
                    self.platforms.append(p)
                    self.entities.add(p)
                elif col == "E":
                    e = ExitBlock(x, y, self._ss_rpg)
                    self.platforms.append(e)
                    self.entities.add(e)
                else:
                    p = Tile(x, y, self._ss_rpg)
                    self.platforms.append(p)
                    self.map.add(p)
                x += 64
            y += 64
            x = 0
        self.total_level_width = len(self.level[0]) * 64
        self.total_level_height = len(self.level) * 64
        self.entities.add(self.player)
        self._init_music()

    def run(self, camera):
        is_running = True
        pygame.key.set_repeat(50, 50)
        while is_running:
            self.timer.tick(60)

            for e in pygame.event.get():
                if e.type == QUIT:
                    raise SystemExit
                if e.type == KEYDOWN and e.key == K_ESCAPE:
                    raise SystemExit
                #else:
                #    self.player.control(e)

            if pygame.key.get_focused():
                pressed = pygame.key.get_pressed()
                self.player.control(pressed)

            # draw background
            for y in range(64):
                for x in range(64):
                    self.screen.blit(self.bg, (x * 64, y * 64))

            self.camera.update(self.player)

            # update player, draw everything else
            self.player.update(self.platforms)

            for t in self.map:
                self.screen.blit(t.image, camera.apply(t))

            for e in self.entities:
                self.screen.blit(e.image, camera.apply(e))

            #draw head's up display
            # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
            hud_font = pygame.font.SysFont("monospace", 16)
            hud_font.set_bold(True)

            # HP
            label = hud_font.render("HP", 1, (255, 0, 0))
            self.screen.blit(label, (2, 4))
            pygame.draw.rect(self.screen, (255, 0, 0), (32, 9, 128, 8))
            # MP
            label = hud_font.render("MP", 1, (0, 0, 255))
            self.screen.blit(label, (2, 20))
            pygame.draw.rect(self.screen, (0, 0, 255), (32, 24, 128, 8))
            # XP
            label = hud_font.render("XP", 1, (0, 255, 0))
            self.screen.blit(label, (2, 38))
            pygame.draw.rect(self.screen, (0, 255, 0), (32, 42, 128, 8))

            self.pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()