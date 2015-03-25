from __future__ import print_function

"Le module definit les ennemies posssible a rencontrer"


from librpg.mapobject import MapObject
from librpg.movement import *
from librpg.locals import *

from action import *


class Enemy(MapObject):
    def __init__(self, map):
        MapObject.__init__(self, MapObject.OBSTACLE,
                           image_file='hulk.png')
        self.map = map
        self.hp = 256
        self.action = Face(DOWN)
        self.emousser = 1.0

    def update_position(self, position):
        self.position = position

    def update(self):
        pass


class Hero(Enemy):
    def __init__(self):
        self.hp = 64
        self.action = Wait(10)
        self.emousser = 1.0
        self.map_object = None

    def ref(self, map_object):
        self.map_object = map_object


class Common(Enemy):
    def __init__(self, map, hero):
        MapObject.__init__(self, MapObject.OBSTACLE,
                           image_file='hulk.png')
        Enemy.__init__(self, map)
        self.hero = hero
        self.action = Attack

    def update(self):
        # print("pos hero: %s et pos monstre %s" % (self.hero.action, self.action))
        if self.hp <= 0:
            print (u'Le monstre est mort.')
            self.destroy()

    def activate(self, party_avatar, direction):
        # self.action = Attack((self, self.position), (self.hero, self.hero.map_object.position))
        # self.schedule_movement(self.action, False)
        self.hero.action = Attack((self.hero, self.hero.map_object.position), (self, self.position))
        self.hero.map_object.schedule_movement(self.hero.action, False)

    def collide_with_party(self, party_avatar, direction):
        self.action = Attack((self, self.position), (self.hero, self.hero.map_object.position))
        self.hero.action = Defence((self.hero, self.hero.map_object.position), (self, self.position))


class Boss(Enemy):
    def __init__(self, map):
        MapObject.__init__(self, MapObject.OBSTACLE,
                           image_file='hulk.png')



__author__ = 'plperron'
