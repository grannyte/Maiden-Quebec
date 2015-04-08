from __future__ import print_function

"Le module definit les ennemies posssible a rencontrer"

HP_INITIAL = 100
PARTY = 0

import time
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
                self.action = Attack((self, self.position), (self.hero, self.hero.map_object.position))
                self.schedule_movement(self.action, False)
            elif "Defence" == next_action:
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


class Monster(BayesMonster):
    def __init__(self, map, hero):
        BayesMonster.__init__(self, map, hero)
        self.movement_behavior.movements.extend([Wait(30), ForcedStep(LEFT),
                                                 Wait(2), ForcedStep(UP),
                                                 Wait(2), ForcedStep(DOWN),
                                                 Wait(2), ForcedStep(DOWN),
                                                 Wait(2), ForcedStep(UP),
                                                 Wait(30), ForcedStep(RIGHT)])
        self.hp = HP_INITIAL

    def update(self):
        pass


class Guard(BayesMonster):
    def __init__(self, map, hero):
        BayesMonster.__init__(self, map, hero)
        self.movement_behavior.movements.extend([])
        self.hp = HP_INITIAL

    def update(self):
        BayesMonster.update(self)
        pass


class CrazyMonster(BayesMonster):
    def __init__(self, map, hero):
        BayesMonster.__init__(self, map, hero)
        self.movement_behavior.movements.extend([])
        self.hp = HP_INITIAL
        self.map = map
        self.party_position = self.map.objects[PARTY].position

    def activate(self, party_avatar, direction):
        BayesMonster.activate(self, party_avatar, direction)

    def collide_with_party(self, party_avatar, direction):
        BayesMonster.collide_with_party(self, party_avatar, direction)

    def update(self):
        # Code laid mais au moins on peut tester!
        BayesMonster.update(self)
        if self.map.objects[PARTY].position.x != self.party_position.x or self.map.objects[PARTY].position.y != self.party_position.y:
            self.party_position = self.map.objects[PARTY].position
            if self.position.x > self.party_position.x:
                self.schedule_movement(ForcedStep(LEFT), True)
            elif self.position.x < self.party_position.x:
                self.schedule_movement(ForcedStep(RIGHT), True)

            if self.position.y > self.party_position.y:
                self.schedule_movement(ForcedStep(UP), True)
            elif self.position.y < self.party_position.y:
                self.schedule_movement(ForcedStep(DOWN), True)
        BayesMonster.update(self)


class SmartMonster(BayesMonster):
    SECONDS_TO_WAIT = 10
    GUARD_WALK = 1
    GUARD_OBSERVE = 2
    GUARD_ATTACK = 3

    def __init__(self, map, hero):
        BayesMonster.__init__(self, map, hero)
        self.state = SmartMonster.GUARD_WALK
        self.corner = (8, 1)
        self.last_time = time.time()

    def update(self):
        if (time.time() - self.last_time > SmartMonster.SECONDS_TO_WAIT):
            self.state = SmartMonster.GUARD_ATTACK

        if (self.state == SmartMonster.GUARD_WALK):
            self.schedule_movement(ForcedStep(DOWN), False)
            self.schedule_movement(Wait(10), False)
            self.schedule_movement(ForcedStep(LEFT), False)
            self.schedule_movement(Wait(10), False)
            self.schedule_movement(ForcedStep(UP), False)
            self.schedule_movement(Wait(10), False)
            self.schedule_movement(ForcedStep(RIGHT), False)
            self.schedule_movement(Wait(10), False)

            proximity = self.detect_proximity()
            if (proximity != 0):
                self.state = SmartMonster.GUARD_OBSERVE
        elif (self.state == SmartMonster.GUARD_OBSERVE):
            self.goto_corner()
        elif (self.state == SmartMonster.GUARD_ATTACK and self.detect_proximity() == 0):
            self.move_to_hero()
        else:
            self.face_hero()
            BayesMonster.update(self)

    def face_hero(self):
        proximity = self.detect_proximity()

        if (proximity == LEFT):
            self.schedule_movement(Face(LEFT), False)
        elif (proximity == RIGHT):
            self.schedule_movement(Face(RIGHT), False)
        elif (proximity == UP):
            self.schedule_movement(Face(UP), False)
        else:
            self.schedule_movement(Face(DOWN), False)

    def goto_corner(self):
        x, _ = self.corner
        if (x == 8):
            self.goto_up_right_corner()
        else:
            self.goto_down_left_corner()

    def goto_up_right_corner(self):
        x, y = self.corner

        if (self.detect_proximity() == RIGHT):
            self.schedule_movement(ForcedStep(UP), True)
        elif (self.position.x != x):
            self.schedule_movement(ForcedStep(RIGHT), True)
        elif (self.position.y != y):
            self.schedule_movement(ForcedStep(UP), True)
        else:
            self.schedule_movement(Face(DOWN), True)
            proximity = self.detect_proximity()
            if (proximity != 0):
                self.corner = (1, 8)

    def goto_down_left_corner(self):
        x, y = self.corner

        # If the party is in the way, change row
        if (self.detect_proximity() == LEFT):
            self.schedule_movement(ForcedStep(DOWN), True)
        elif (self.position.x != x):
            self.schedule_movement(ForcedStep(LEFT), True)
        elif (self.position.y != y):
            self.schedule_movement(ForcedStep(DOWN), True)
        else:
            self.schedule_movement(Face(UP), True)
            proximity = self.detect_proximity()
            if (proximity != 0):
                self.corner = (8, 1)

    def detect_proximity(self):
        if (self.position.x == self.map.objects[PARTY].position.x and
                    self.position.y == self.map.objects[PARTY].position.y + 1):
            return UP
        elif (self.position.x == self.map.objects[PARTY].position.x and
                      self.position.y == self.map.objects[PARTY].position.y - 1):
            return DOWN
        elif (self.position.y == self.map.objects[PARTY].position.y and
                      self.position.x == self.map.objects[PARTY].position.x + 1):
            return LEFT
        elif (self.position.y == self.map.objects[PARTY].position.y and
                      self.position.x == self.map.objects[PARTY].position.x - 1):
            return RIGHT
        else:
            return 0

    def move_to_hero(self):
            if (self.position.x > self.map.objects[PARTY].position.x):
                self.schedule_movement(ForcedStep(LEFT), True)
            elif (self.position.x < self.map.objects[PARTY].position.x):
                self.schedule_movement(ForcedStep(RIGHT), True)

            if (self.position.y > self.map.objects[PARTY].position.y):
                self.schedule_movement(ForcedStep(UP), True)
            elif (self.position.y < self.map.objects[PARTY].position.y):
                self.schedule_movement(ForcedStep(DOWN), True)
