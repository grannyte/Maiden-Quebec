from __future__ import print_function

"Le module definit les ennemies posssible a rencontrer"


HP_INITIAL = 100
PARTY = 0


GUARD_WALK = 1
GUARD_OBSERVE = 2


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


hero = Hero()

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





class Monster(MapObject):
    def __init__(self):
        MapObject.__init__(self, MapObject.OBSTACLE,
                           image_file='hulk.png')
        self.movement_behavior.movements.extend([Wait(30), ForcedStep(LEFT),
                                                 Wait(2), ForcedStep(UP),
                                                 Wait(2), ForcedStep(DOWN),
                                                 Wait(2), ForcedStep(DOWN),
                                                 Wait(2), ForcedStep(UP),
                                                 Wait(30), ForcedStep(RIGHT)])
        self.hp = HP_INITIAL

    def activate(self, party_avatar, direction):
        self.hp -= 10
        print(u'Attaque du monstre (-10) [' + str(self.hp) + '/' + str(HP_INITIAL) + ']')
        if (self.hp <= 0):
            print(u'Le monstre est mort.')
            self.destroy()

    def collide_with_party(self, party_avatar, direction):
        hero.hp -= 10
        self.schedule_movement(Wait(5))
        if hero.hp <= 0:
            print("die bitch")
        print(hero.hp)

    def update(self):
        pass


class Guard(MapObject):
    def __init__(self):
        MapObject.__init__(self, MapObject.OBSTACLE,
                           image_file='hulk.png')
        self.movement_behavior.movements.extend([])
        self.hp = HP_INITIAL

    def activate(self, party_avatar, direction):
        self.hp -= 10
        print(u'Attaque du monstre (-10) [' + str(self.hp) + '/' + str(HP_INITIAL) + ']')
        if (self.hp <= 0):
            print(u'Le monstre est mort.')
            self.destroy()

    def collide_with_party(self, party_avatar, direction):
        print('defense')

    def update(self):
        pass


class CrazyMonster(MapObject):
    def __init__(self, map):
        MapObject.__init__(self, MapObject.OBSTACLE,
                           image_file='hulk.png')
        self.movement_behavior.movements.extend([])
        self.hp = HP_INITIAL
        self.map = map
        self.party_position = self.map.objects[PARTY].position

    def activate(self, party_avatar, direction):
        self.hp -= 10
        print(u'Attaque du monstre (-10) [' + str(self.hp) + '/' + str(HP_INITIAL) + ']')
        if (self.hp <= 0):
            print(u'Le monstre est mort.')
            self.destroy()

    def collide_with_party(self, party_avatar, direction):
        print('defense')

    def update(self):
        # Code laid mais au moins on peut tester!
        if (self.map.objects[PARTY].position.x != self.party_position.x or
                    self.map.objects[PARTY].position.y != self.party_position.y):
            self.party_position = self.map.objects[PARTY].position
            if (self.position.x > self.party_position.x):
                self.schedule_movement(ForcedStep(LEFT), False)
            elif (self.position.x < self.party_position.x):
                self.schedule_movement(ForcedStep(RIGHT), False)

            if (self.position.y > self.party_position.y):
                self.schedule_movement(ForcedStep(UP), False)
            elif (self.position.y < self.party_position.y):
                self.schedule_movement(ForcedStep(DOWN), False)


class SmartMonster(MapObject):
    def __init__(self, map):
        MapObject.__init__(self, MapObject.OBSTACLE,
                           image_file='hulk.png')
        self.movement_behavior.movements.extend([])
        self.hp = HP_INITIAL
        self.map = map
        self.party_position = self.map.objects[PARTY].position
        self.state = GUARD_WALK
        self.corner = (8, 1)

    def activate(self, party_avatar, direction):
        self.hp -= 10
        print(u'Attaque du monstre (-10) [' + str(self.hp) + '/' + str(HP_INITIAL) + ']')
        if (self.hp <= 0):
            print(u'Le monstre est mort.')
            self.destroy()

    def collide_with_party(self, party_avatar, direction):
        print('defense')

    def update(self):
        if (self.state == GUARD_WALK):
            self.map.monster.schedule_movement(ForcedStep(DOWN), False)
            self.map.monster.schedule_movement(Wait(10), False)
            self.map.monster.schedule_movement(ForcedStep(LEFT), False)
            self.map.monster.schedule_movement(Wait(10), False)
            self.map.monster.schedule_movement(ForcedStep(UP), False)
            self.map.monster.schedule_movement(Wait(10), False)
            self.map.monster.schedule_movement(ForcedStep(RIGHT), False)
            self.map.monster.schedule_movement(Wait(10), False)

            proximity = self.detect_proximity()
            if (proximity != 0):
                self.state = GUARD_OBSERVE
                self.map.monster.schedule_movement(Wait(2), True)
        else:
            self.goto_corner()

    def goto_corner(self):
        x, _ = self.corner
        if (x == 8):
            self.goto_up_right_corner()
        else:
            self.goto_down_left_corner()

    def goto_up_right_corner(self):
        x, y = self.corner

        if (self.detect_proximity() == RIGHT):
            self.map.monster.schedule_movement(ForcedStep(UP), True)
        elif (self.map.monster.position.x != x):
            self.map.monster.schedule_movement(ForcedStep(RIGHT), True)
        elif (self.map.monster.position.y != y):
            self.map.monster.schedule_movement(ForcedStep(UP), True)
        else:
            self.map.monster.schedule_movement(Face(DOWN), True)
            proximity = self.detect_proximity()
            if (proximity != 0):
                self.corner = (1, 8)

    def goto_down_left_corner(self):
        x, y = self.corner

        # If the party is in the way, change row
        if (self.detect_proximity() == LEFT):
            self.map.monster.schedule_movement(ForcedStep(DOWN), True)
        elif (self.map.monster.position.x != x):
            self.map.monster.schedule_movement(ForcedStep(LEFT), True)
        elif (self.map.monster.position.y != y):
            self.map.monster.schedule_movement(ForcedStep(DOWN), True)
        else:
            self.map.monster.schedule_movement(Face(UP), True)
            proximity = self.detect_proximity()
            if (proximity != 0):
                self.corner = (8, 1)

    def detect_proximity(self):
        if (self.map.monster.position.x == self.map.objects[PARTY].position.x and
                    self.map.monster.position.y == self.map.objects[PARTY].position.y + 1):
            return UP
        elif (self.map.monster.position.x == self.map.objects[PARTY].position.x and
                      self.map.monster.position.y == self.map.objects[PARTY].position.y - 1):
            return DOWN
        elif (self.map.monster.position.y == self.map.objects[PARTY].position.y and
                      self.map.monster.position.x == self.map.objects[PARTY].position.x + 1):
            return LEFT
        elif (self.map.monster.position.y == self.map.objects[PARTY].position.y and
                      self.map.monster.position.x == self.map.objects[PARTY].position.x - 1):
            return RIGHT
        else:
            return 0





#class Boss(Enemy):
#    def __init__(self, map):
#        MapObject.__init__(self, MapObject.OBSTACLE,
#                           image_file='hulk.png')



__author__ = 'plperron'
