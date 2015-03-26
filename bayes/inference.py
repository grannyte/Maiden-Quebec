"""
Imitate Bayesian network with hardcoded rule
"""

import random

class Bayes:
    def __init__(self, monstre, hero):
        self.monstre = monstre
        self.hero = hero
        self.network = {
            "EnemyHP": {"parent": [], "nodes": [(.5, "more"), (.5, "less")]},
            "EnemyErode": {"parent": [], "nodes": [(.5, "more"), (.5, "less")]},
            "EnemyAction": {"parent": ["EnemyHP", "EnemyErode"], "nodes": [
                (.5, "more", "more", "Attack"),
                (.5, "more", "more", "Defence"),
                (.1, "more", "less", "Attack"),
                (.9, "more", "less", "Defence"),
                (.9, "less", "more", "Attack"),
                (.1, "less", "more", "Defence"),
                (.25, "less", "less", "Attack"),
                (.75, "less", "less", "Defence"),
            ]
            },
        }

    def next_action(self, believe_hp, believe_erode):
        actions = self.network["EnemyAction"]["nodes"][:]
        actions = filter(lambda x: x[1] == believe_hp, actions)
        actions = filter(lambda x: x[2] == believe_erode, actions)
        actions = [(action[3], action[0]) for action in actions]
        return weighted_choice(actions)


def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = random.uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w > r:
         return c
      upto += w
   assert False, "Shouldn't get here"

__author__ = 'plperron'
