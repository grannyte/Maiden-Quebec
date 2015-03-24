from __future__ import print_function

"""
Le module définit les actions nécessaires au bon déroulement du jeu.
"""


class Action(object):
    pass


class Move(Action):
    pass


class Fight(Action):
    pass


class Attack(Fight):
    pass


class Defence(Fight):
    pass


class Counter(Fight):
    pass

__author__ = 'plperron'
