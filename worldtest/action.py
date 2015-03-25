from __future__ import print_function

"""
Le module definit les actions necessaires au bon deroulement du jeu.
"""

from librpg.movement import Face, Wait, ForcedStep
from librpg.locals import *
from librpg.movement import *


class Fight(Movement):

    def __init__(self, enemy1, enemy2):
        self.enemy1, self.pos1 = enemy1
        self.enemy2, self.pos2 = enemy2

    def flow(self, obj):
        if euclidian_distance(self.pos1, self.pos2) == 1:
            print("enemy1 %s and enemy2 %s" % (type(self.enemy1.action).__name__, type(self.enemy2.action).__name__))
            interaction(self.enemy1, self.enemy2)
            interaction(self.enemy2, self.enemy1)
            if isinstance(self.enemy1.action, Fight):
                self.enemy1.action = Wait(8)
            if isinstance(self.enemy2.action, Fight):
                self.enemy2.action = Wait(8)
            try:
                self.enemy1.schedule_movement(self.enemy1.action, False)
            except AttributeError:
                self.enemy1.map_object.schedule_movement(self.enemy1.action, False)
            try:
                self.enemy2.schedule_movement(self.enemy2.action, False)
            except AttributeError:
                self.enemy2.map_object.schedule_movement(self.enemy2.action, False)
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
        enemy1.emousser *= 0.95
        enemy2.emousser *= 0.95
        enemy1.counters["pared"] += 1
        enemy2.counters["pared"] += 1
    elif type(enemy1.action).__name__ == "Attack" and type(enemy2.action).__name__ == "Defence":
        enemy1.emousser *= 0.85
        enemy2.hp -= enemy1.emousser * 2
        enemy1.counters["blocked"] += 1
    elif type(enemy1.action).__name__ == "Attack":
        enemy2.hp -= enemy1.emousser * 8
        enemy2.counters["cutted"] += 1

__author__ = 'plperron'
