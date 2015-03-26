from __future__ import print_function

"Le module definit les ennemies posssible a rencontrer"


from librpg.mapobject import MapObject
from librpg.movement import *
from librpg.locals import *

from action import *
from bayes.inference import *


class Enemy(MapObject):
    def __init__(self, map):
        MapObject.__init__(self, MapObject.OBSTACLE,
                           image_file='hulk.png')
        self.map = map
        self.hp = 100
        self.action = Face(DOWN)
        self.emousser = 1.0
        self.counters = {"cutted": 0, "blocked": 0, "pared": 0}

    def update_position(self, position):
        self.position = position

    def update(self):
        pass


class Hero(Enemy):
    def __init__(self):
        self.hp = 100
        self.action = Wait(10)
        self.emousser = 1.0
        self.counters = {"cutted": 0, "blocked": 0, "pared": 0}
        self.map_object = None

    def ref(self, map_object):
        self.map_object = map_object


class BayesMonster(Enemy):
    def __init__(self, map, hero):
        MapObject.__init__(self, MapObject.OBSTACLE,
                           image_file='hulk.png')
        Enemy.__init__(self, map)
        self.hero = hero
        self.hero.counters = {"cutted": 0, "blocked": 0, "pared": 0} #reset
        self.bayes = Bayes(self, self.hero)
        self.action = Attack((self, self.position), (self.hero, self.hero.map_object.position))
        self.map = map
        self.count = 5

    def update(self):
        if(self.count <= 0):
            next_action = random.choice(["Attack", "Defence"]) #self.bayes.next_action(self.estimate_enemy_hp(), self.estimate_enemy_erode())
            if "Attack" == next_action:
                print("1")
                self.action = Attack((self, self.position), (self.hero, self.hero.map_object.position))
                self.schedule_movement(self.action, False)
            elif "Defence" == next_action:
                print("2")
                self.action = Defence((self, self.position), (self.hero, self.hero.map_object.position))
                self.schedule_movement(self.action, False)

            print("HERO:"+ str(round(self.hero.hp)) +" MONSTER:"+ str(round(self.hp,0)))
            print("HERO EMOUSSER: " + str(self.hero.emousser) + " MONSTER EMOUSSER: " + str(self.emousser))

            if self.hp <= 1:
                print (u'Le monstre est mort.')
                self.destroy()

            if self.hero.hp <= 1:
                print("Vous etes mort")
                self.map.gameover()

            self.count = 5
        self.count -= 1

    def estimate_enemy_hp(self):
        return "more" if self.hero.counters["cutted"] < self.counters["cutted"] else "less"

    def estimate_enemy_erode(self):
        h = self.hero.counters["blocked"] + self.hero.counters["pared"]
        m = self.hero.counters["blocked"] + self.hero.counters["pared"]
        return "more" if h > m else "less"

    def activate(self, party_avatar, direction):
        self.hero.action = Attack((self.hero, self.hero.map_object.position), (self, self.position))
        self.hero.map_object.schedule_movement(self.hero.action, False)

    def collide_with_party(self, party_avatar, direction):
        self.hero.action = Defence((self.hero, self.hero.map_object.position), (self, self.position))
        self.hero.map_object.schedule_movement(self.hero.action, False)


#class Boss(Enemy):
#    def __init__(self, map):
#        MapObject.__init__(self, MapObject.OBSTACLE,
#                           image_file='hulk.png')



__author__ = 'plperron'
