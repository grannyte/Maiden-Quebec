from __future__ import print_function

"""
Le module définit les actions nécessaires au bon déroulement du jeu.
"""

from librpg.movement import Face, Wait, ForcedStep
from librpg.locals import *

class Action(object):
    def act(self):
        pass


class Move(Action):
    def act(self):
        pass


class Step(Move):
    def act(self, direction):
        """

        :param direction: either UP, DOWN, LEFT, RIGHT
        :return:
        """
        return ForcedStep(direction)


class Fight(Action):
    pass


class Attack(Fight):
    pass


class Defence(Fight):
    pass


class Counter(Fight):
    pass

__author__ = 'plperron'
