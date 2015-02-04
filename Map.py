
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
        turtle = Turtle(pygame.math.Vector2(len(l_map)/2, len(l_map[0])/2), pygame.math.Vector2(1, 0))
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

