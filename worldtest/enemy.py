from __future__ import print_function

"Le module definit les ennemies posssible a rencontrer"


from librpg.mapobject import MapObject
from librpg.movement import *
from librpg.locals import *


class Enemy(MapObject):
    def __init__(self, map):
        MapObject.__init__(self, MapObject.OBSTACLE,
                           image_file='hulk.png')
        self.map = map
        self.hp = 16
        self.action = Face(DOWN)
        self.emousser = 1.0

    def update_position(self, position):
        self.position = position

    def update(self):
        pass


class Hero(Enemy):
    def __init__(self):
        self.hp = 64
        self.action = "still"
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
        self.action = "attack"

    def update(self):
        print("pos hero: %s et pos monstre %s" % (self.hero.action, self.action))
        if euclidian_distance(self.hero.map_object.position, self.position) == 1:
            if self.hero.action != "still" or self.action != "still":
                interaction(self.hero, self)
                interaction(self, self.hero)
                self.hero.action = "still"
                self.action = "still"
                self.hero.map_object.schedule_movement(Wait(10))
                self.schedule_movement(Wait(10))
                if (self.hp <= 0):
                    print (u'Le monstre est mort.')
                    self.destroy()

    def activate(self, party_avatar, direction):
        self.hero.action = "attack"

    def collide_with_party(self, party_avatar, direction):
        self.hero.action = "defence"


class Boss(Enemy):
    def __init__(self, map):
        MapObject.__init__(self, MapObject.OBSTACLE,
                           image_file='hulk.png')


def euclidian_distance(pos1, pos2):
    return abs(((pos1.x - pos2.x) * (pos1.x - pos2.x)) + (pos1.y - pos2.y) * (pos1.y - pos2.y))


def interaction(enemy1, enemy2):
    if enemy1.action != "still" or enemy2.action != "still":
        print("hero: %s et monstre %s" % (enemy1.action, enemy2.action))
    if enemy1.action == "attack" and enemy2.action == "attack":
        enemy1.emousser *= 0.95
        enemy2.emousser *= 0.95
    elif enemy1.action == "attack" and enemy2.action == "defence":
        enemy1.emousser *= 0.85
        enemy2.hp -= enemy1.emousser * 2
    elif enemy1.action == "attack":
        enemy2.hp -= enemy1.emousser * 8
    elif enemy1.action == "defence" and enemy2.action  == "attack":
        enemy1.hp -= enemy1.emousser * 2
        enemy2.emousser *= 0.85
    print(enemy1.hp)
    print(enemy2.hp)


__author__ = 'plperron'
