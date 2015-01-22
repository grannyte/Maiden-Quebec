
import pygame
from pygame import *
import math

def create_level():
    return [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "P       S            PPPPPPPPPPP           P",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "P    PPPPPPPPP      P PPP                  P",
        "P            P      P S P                  P",
        "P            P      P   P  PPPPPPP         P",
        "PPPP         P   PPPPPPPPPPP               P",
        "P            P   P     P                   P",
        "P         PPPPPPPP PPPPS                   P",
        "P                P   P                     P",
        "P                P PPPPPPPPPP              P",
        "P                P          P              P",
        "P   PPPPPPPPPPPPPPPPPPPPPP  P              P",
        "P                P E        P              P",
        "P                PPPPPPPPPPPP              P",
        "P                                          P",
        "PPPPPPPP                                   P",
        "P                                          P",
        "P                                          P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        ]


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
        self._heading_stack.append(self.heading)

    def memorise_position(self):
        self._position_stack.append(self.position)

    def memorise_position_and_heading(self):
        self._position_stack.append(self.position)
        self._heading_stack.append(self.heading)

    def last_position(self):
        self.position = self._position_stack.pop()


    def last_heading(self):
        self.heading = self._heading_stack.pop()


    def last_position_and_heading(self):
        self.position = self._position_stack.pop()
        self.heading = self._heading_stack.pop()


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
                self.unfolded[-1].replace(c.marker, c.unfold)

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
        turtle = Turtle(pygame.math.Vector2(0, 0), pygame.math.Vector2(1, 0))
        l_map[int(turtle.position.x)][int(turtle.position.y)] = self.unfolded[-1][-1]