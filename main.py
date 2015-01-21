import pygame
from pygame import *
from player import Player
from tile import Tile
from exitblock import ExitBlock
from camera import ComplexCamera
from map import create_level
from Spike import Spike
from Walls import Walls

WIN_WIDTH = 800
WIN_HEIGHT = 640
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

def main():
    global cameraX, cameraY
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    pygame.display.set_caption("Use arrows to move!")
    timer = pygame.time.Clock()

    bg = Surface((32, 32))
    bg.convert()
    bg.fill(Color("#000000"))
    map = pygame.sprite.Group()
    entities = pygame.sprite.Group()
    player = Player(32, 32)
    platforms = []

    x = y = 0
    level = create_level()

    # build the level
    for row in level:
        for col in row:
            if col == "P":
                p = Walls(x, y)
                platforms.append(p)
                entities.add(p)
            elif col == "S":
                p = Spike(x, y)
                platforms.append(p)
                entities.add(p)
            elif col == "E":
                e = ExitBlock(x, y)
                platforms.append(e)
                entities.add(e)
            else:
                p = Tile(x, y)
                platforms.append(p)
                map.add(p)
            x += 32
        y += 32
        x = 0

    total_level_width = len(level[0])*32
    total_level_height = len(level)*32
    camera = ComplexCamera(total_level_width, total_level_height, WIN_WIDTH, WIN_HEIGHT)
    entities.add(player)

    is_running = True
    while is_running:
        timer.tick(60)

        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit
            else:
                player.control(e, platforms)

        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        camera.update(player)

        # update player, draw everything else
        player.update()

        for t in map:
            screen.blit(t.image, camera.apply(t))

        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update()

if __name__ == "__main__":
    main()