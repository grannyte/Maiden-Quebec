# -*- coding: utf-8 -*-

import pygame
from pygame import *
from mymaps import*
import csv

class Gene():
    def __init__(self, marker, unfold):
        self.marker = marker
        self.unfold = unfold


class Turtle():
    def __init__(self, position, heading):
        self.position = position
        self.heading = heading
        self._position_stack = []
        self._heading_stack = []

    def memorise_heading(self):
        self._heading_stack.append(pygame.math.Vector2(self.heading))

    def memorise_position(self):
        self._position_stack.append(pygame.math.Vector2(self.position))

    def memorise_position_and_heading(self):
        self._position_stack.append(pygame.math.Vector2(self.position))
        self._heading_stack.append(pygame.math.Vector2(self.heading))

    def last_position(self):
        self.position = self._position_stack[-1]
        del self._position_stack[-1]

    def last_heading(self):
        self.heading = self._heading_stack[-1]
        del self._heading_stack[-1]

    def last_position_and_heading(self):
        self.position = self._position_stack[-1]
        del self._position_stack[-1]
        self.heading = self._heading_stack[-1]
        del self._heading_stack[-1]


class LSystemMap():
    def __init__(self, iterations, dna):
        self.iterations = iterations
        self.dna = dna
        self.chromozomes = []
        self.unfolded = []

    def append_gene(self, gene):
        self.chromozomes.append(gene)

    def unfold(self):
        self.unfolded.append(self.dna)
        for iteration in range(0, self.iterations):
            self.unfolded.append(self.unfolded[-1])
            for c in self.chromozomes:
                self.unfolded[-1] = self.unfolded[-1].replace(c.marker, c.unfold)

    def buildmap(self, sizex, sizey):
        l_map = []
        for x in range(0, sizex):
            l_map.append(list(""))
            for y in range(0, sizey):
                l_map[x] += 'P'
        self.unfold()
        self.interpret(l_map)
        return l_map

    def interpret(self, l_map):
        turtle = Turtle(pygame.math.Vector2(len(l_map)/4, len(l_map[0])/4), pygame.math.Vector2(1, 0))
        for p in self.unfolded[-1]:
            if l_map[min(max(int(turtle.position.x), 0), len(l_map)-1)][min(max(int(turtle.position.y), 0), len(l_map)-1)] != 'E':
                l_map[min(max(int(turtle.position.x), 0), len(l_map)-1)][min(max(int(turtle.position.y), 0), len(l_map)-1)] = p
            if p == '>':
                turtle.heading.rotate_ip(90)
            elif p == '<':
                turtle.heading.rotate_ip(-90)
            elif p == '[':
                turtle.memorise_position()
            elif p == ']':
                turtle.last_position()
            elif p == '(':
                turtle.memorise_heading()
            elif p == ')':
                turtle.last_heading()
            elif p == '{':
                turtle.memorise_position_and_heading()
            elif p == '}':
                turtle.last_position_and_heading()
            turtle.position += turtle.heading


class LSystemMap(WorldMap):
    def __init__(self):
        a = [[10, 10, 1],
             [],
             [65, 65, 65, 65, 65, 65, 65, 65, 65, 65],
             [65, 65, 65, 65, 65, 65, 65, 65, 65, 65],
             [65, 65, 65, 65, 65, 65, 65, 65, 65, 65],
             [65, 65, 65, 65, 65, 65, 65, 65, 65, 65],
             [65, 65, 65, 65, 65, 65, 65, 65, 65, 65],
             [65, 65, 65, 65, 65, 65, 65, 65, 65, 65],
             [65, 65, 65, 65, 65, 65, 65, 65, 65, 65],
             [65, 65, 65, 65, 65, 65, 65, 65, 65, 65],
             [65, 65, 65, 65, 65, 65, 65, 65, 65, 65],
             [65, 65, 65, 65, 65, 65, 65, 65, 65, 65],
             [],
             [13, 13, 13, 13, 0, 0, 13, 13, 13, 13],
             [23, 23, 23, 23, 0, 0, 23, 23, 23, 23],
             [13, 0, 0, 0, 0, 0, 0, 0, 0, 13],
             [23, 0, 0, 0, 0, 0, 0, 0, 0, 23],
             [13, 0, 0, 0, 0, 0, 0, 0, 0, 13],
             [23, 0, 0, 0, 0, 0, 0, 0, 0, 23],
             [13, 0, 0, 0, 0, 0, 0, 0, 0, 13],
             [23, 0, 0, 0, 0, 0, 0, 0, 0, 23],
             [13, 13, 13, 13, 13, 13, 13, 13, 13, 13],
             [23, 23, 23, 23, 23, 23, 23, 23, 23, 23]]
        with open("worldtest/LSystem.map", "wb") as f:
            writer = csv.writer(f)
            writer.writerows(a)
        WorldMap.__init__(self, 'worldtest/LSystem.map',
                          LOWER_TILESET,
                          UPPER_TILESET)

    def initialize(self, local_state, global_state):
        self.add_area(RelativeTeleportArea(y_offset=+8, map_id=2), RectangleArea((4, 0), (5, 0)))


        self.monster = CrazyMonster(self)
        self.add_object(self.monster, Position(7, 7))
        self.monster1 = CrazyMonster(self)
        self.add_object(self.monster1, Position(3, 3))
        self.monster2 = CrazyMonster(self)
        self.add_object(self.monster2, Position(3, 7))
        self.monster3 = CrazyMonster(self)
        self.add_object(self.monster3, Position(4, 7))
        self.monster4 = CrazyMonster(self)
        self.add_object(self.monster4, Position(5, 7))
        self.monster5 = CrazyMonster(self)
        self.add_object(self.monster5, Position(6, 7))
        self.monster6 = CrazyMonster(self)
        self.add_object(self.monster6, Position(3, 6))

        hero.update_position(self.objects[PARTY].position)
        hero.ref(self.objects[PARTY])
        print(hero.position)
