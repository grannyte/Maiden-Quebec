from __future__ import print_function

"""
Le module definit les actions necessaires au bon deroulement du jeu.
"""

from librpg.movement import Face, Wait, ForcedStep
from librpg.locals import *
from librpg.movement import *


class Fight(Movement):
    DAMAGE = 10

    def __init__(self, enemy1, enemy2):
        self.enemy1, self.pos1 = enemy1
        self.enemy2, self.pos2 = enemy2

    def flow(self, obj):
        if euclidian_distance(self.pos1, self.pos2) == 1:
            print("enemy1 %s and enemy2 %s" % (type(self.enemy1.action).__name__, type(self.enemy2.action).__name__))
            interaction(self.enemy1, self.enemy2)
            interaction(self.enemy2, self.enemy1)
            self.enemy1.action = ""
            self.enemy2.action = ""
        return True, True


class Attack(Fight):
    def __init__(self, enemy1, enemy2):
        Fight.__init__(self, enemy1, enemy2)

    def flow(self, obj):
        return Fight.flow(self, obj)


class Defence(Fight):
    def __init__(self, enemy1, enemy2):
        Fight.__init__(self, enemy1, enemy2)

    def flow(self, obj):
        return Fight.flow(self, obj)


class Counter(Fight):
    def __init__(self, enemy1, enemy2):
        Fight.__init__(self, enemy1, enemy2)

    def flow(self, obj):
        return Fight.flow(self, obj)



def euclidian_distance(pos1, pos2):
    return abs(((pos1.x - pos2.x) * (pos1.x - pos2.x)) + (pos1.y - pos2.y) * (pos1.y - pos2.y))


def interaction(enemy1, enemy2):
    if type(enemy1.action).__name__ == "Attack" and type(enemy2.action).__name__ == "Attack":
        enemy1.emousser *= 0.99
        enemy2.emousser *= 0.99
        enemy1.counters["pared"] += 1
        enemy2.counters["pared"] += 1
    elif type(enemy1.action).__name__ == "Attack" and type(enemy2.action).__name__ == "Defence":
        enemy1.emousser *= 0.99
        enemy2.hp -= (Fight.DAMAGE*enemy1.emousser)
        enemy1.counters["blocked"] += 1
    elif type(enemy1.action).__name__ == "Attack":
        enemy1.emousser *= 0.99
        enemy2.hp -= (Fight.DAMAGE*enemy1.emousser)
        enemy2.counters["cutted"] += 1

__author__ = 'plperron'
