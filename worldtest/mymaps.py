# -*- coding: utf-8 -*-

from librpg.world import WorldMap
from librpg.mapobject import ScenarioMapObject, MapObject
from librpg.maparea import RectangleArea, MapArea
from librpg.util import Position
from librpg.movement import Face, Wait, ForcedStep
from librpg.dialog import MessageDialog
from librpg.locals import *
from librpg.path import *
from librpg.collection.maparea import RelativeTeleportArea

from worldtest.enemy import *

hero = Hero()

SAVE_FILE = 'save'
LOWER_TILESET = (tileset_path('city_lower.png'),
                 tileset_path('city_lower.bnd'))
UPPER_TILESET = [(tileset_path('world_upper.png'),
                  tileset_path('world_upper.bnd'))]
HP_INITIAL = 100
HAUT_TOUR = 12
BAS_TOUR = 22
PARTY = 0

GUARD_WALK = 1
GUARD_OBSERVE = 2


class SavePoint(ScenarioMapObject):
    def __init__(self, map):
        ScenarioMapObject.__init__(self, map, 0, 1)
        self.map = map

    def activate(self, party_avatar, direction):
        self.map.schedule_message(
            MessageDialog(u'Votre partie se sauvegarge dans %s.' % SAVE_FILE, block_movement=True))
        self.map.save_world(SAVE_FILE)
        self.map.schedule_message(MessageDialog(u'Partie sauvegardée.', block_movement=True))


class MessagePoint(ScenarioMapObject):
    def __init__(self, map, position, message):
        ScenarioMapObject.__init__(self, map, 0, position)
        self.map = map
        self.message = message

    def activate(self, party_avatar, direction):
        self.map.schedule_message(MessageDialog(self.message, block_movement=True))


class Chest(MapObject):
    def __init__(self, closed=True):
        MapObject.__init__(self, MapObject.OBSTACLE,
                           image_file=charset_path('chest.png'),
                           image_index=0,
                           basic_animation=[[0]])
        if closed:
            self.facing = UP
        self.closed = closed

    def activate(self, party_avatar, direction):
        if self.closed:
            self.closed = False
            self.schedule_movement(Face(RIGHT))
            self.schedule_movement(Wait(2))
            self.schedule_movement(Face(DOWN))
            self.schedule_movement(Wait(2))
            self.schedule_movement(Face(LEFT))
            self.map.sync_movement([self])
        else:
            self.schedule_movement(Face(UP))
            self.closed = True
        print u'Bravo vous avez complété le jeu.'
        self.map.gameover()


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
            if (self.map.monster.position.x > self.party_position.x):
                self.map.monster.schedule_movement(ForcedStep(LEFT), False)
            else:
                self.map.monster.schedule_movement(ForcedStep(RIGHT), False)

            if (self.map.monster.position.y > self.party_position.y):
                self.map.monster.schedule_movement(ForcedStep(UP), False)
            else:
                self.map.monster.schedule_movement(ForcedStep(DOWN), False)


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


class ProtectedArea(MapArea):
    def __init__(self, map, movements):
        self.map = map
        self.movements = movements

    def party_entered(self, party_avatar, position):
        if (self.map.guard.position.x != 2):
            for movement in self.movements:
                self.map.guard.schedule_movement(movement, False)

    def party_moved(self, party_avatar, left_position, entered_position, from_outside):
        pass

    def party_left(self, party_avatar, position):
        pass


class GameOverBarrel(ScenarioMapObject):
    def __init__(self, map):
        ScenarioMapObject.__init__(self, map, 0, 4)

    def activate(self, party_avatar, direction):
        print u'Le barril explose et vous êtes mort.'
        self.map.gameover()


class Map1(WorldMap):
    def __init__(self):
        WorldMap.__init__(self, 'worldtest/map1.map',
                          LOWER_TILESET,
                          UPPER_TILESET)

    def initialize(self, local_state, global_state):
        self.add_area(RelativeTeleportArea(x_offset=-8, map_id=2), RectangleArea((9, 2), (9, 8)))
        self.add_object(MessagePoint(self, HAUT_TOUR,
                                     u'Vieil homme dans la tour: Vous aviez bu trop de Maiden-Quebec et vous avez coulé votre navire.  Les vagues vous ont ramené sur le rivage, comptez vous chanceux d\'être en vie! Vous devriez retourner à la maison maintenant...'),
                        Position(3, 3))
        self.add_object(MessagePoint(self, BAS_TOUR,
                                     u'Vieil homme dans la tour: Vous aviez bu trop de Maiden-Quebec et vous avez coulé votre navire.  Les vagues vous ont ramené sur le rivage, comptez vous chanceux d\'être en vie! Vous devriez retourner à la maison maintenant...'),
                        Position(3, 4))
        hero.update_position(self.objects[PARTY].position)
        hero.ref(self.objects[PARTY])
        print(hero.position)


class Map2(WorldMap):
    def __init__(self):
        WorldMap.__init__(self, 'worldtest/map2.map',
                          LOWER_TILESET,
                          UPPER_TILESET)

    def initialize(self, local_state, global_state):
        print(hero.hp)
        self.add_area(RelativeTeleportArea(x_offset=+8, map_id=1), RectangleArea((0, 2), (0, 7)))
        self.add_area(RelativeTeleportArea(x_offset=-8, map_id=3), RectangleArea((9, 2), (9, 7)))
        self.add_area(RelativeTeleportArea(y_offset=+8, map_id=4), RectangleArea((4, 0), (5, 0)))
        self.add_object(SavePoint(self), Position(5, 2))
        hero.update_position(self.objects[PARTY].position)
        hero.ref(self.objects[PARTY])
        self.monster = BayesMonster(self, hero)
        self.add_object(self.monster, Position(4, 4))
        print("DEBUG" + str(self.monster.position))


class Map3(WorldMap):
    def __init__(self):
        WorldMap.__init__(self, 'worldtest/map3.map',
                          LOWER_TILESET,
                          UPPER_TILESET)

    def initialize(self, local_state, global_state):
        self.add_object(GameOverBarrel(self), Position(9, 3))
        self.add_object(GameOverBarrel(self), Position(9, 7))
        self.add_object(Monster(), Position(8, 5))
        self.add_area(RelativeTeleportArea(x_offset=+8, map_id=2), RectangleArea((0, 3), (0, 6)))

        if local_state is not None:
            self.chest = Chest(local_state['chest_closed'])
        else:
            self.chest = Chest()
        self.add_object(self.chest, Position(9, 5))
        hero.update_position(self.objects[PARTY].position)
        hero.ref(self.objects[PARTY])
        print(hero.position)

    def save_state(self):
        return {'chest_closed': self.chest.closed}


class Map4(WorldMap):
    def __init__(self):
        WorldMap.__init__(self, 'worldtest/map4.map',
                          LOWER_TILESET,
                          UPPER_TILESET)

    def initialize(self, local_state, global_state):
        self.add_area(RelativeTeleportArea(y_offset=-8, map_id=2), RectangleArea((4, 9), (5, 9)))
        self.add_area(RelativeTeleportArea(x_offset=-8, map_id=5), RectangleArea((9, 4), (9, 5)))
        self.add_area(RelativeTeleportArea(y_offset=+8, map_id=6), RectangleArea((8, 0), (8, 0)))

        self.guard = Guard()
        self.add_object(self.guard, Position(8, 3))

        movements = [ForcedStep(LEFT) for _ in range(6)]
        self.add_area(ProtectedArea(self, movements), RectangleArea((1, 5), (1, 5)))

        self.add_object(MessagePoint(self, HAUT_TOUR, u'Sage de la tour: Bravo! Belle idée de venir ici!'),
                        Position(1, 5))
        self.add_object(MessagePoint(self, BAS_TOUR, u'Sage de la tour: Bravo! Belle idée de venir ici!'),
                        Position(1, 6))
        hero.update_position(self.objects[PARTY].position)
        hero.ref(self.objects[PARTY])
        print(hero.position)


class Map5(WorldMap):
    def __init__(self):
        WorldMap.__init__(self, 'worldtest/map5.map',
                          LOWER_TILESET,
                          UPPER_TILESET)

    def initialize(self, local_state, global_state):
        self.add_area(RelativeTeleportArea(x_offset=+8, map_id=4), RectangleArea((0, 4), (0, 5)))

        self.monster = CrazyMonster(self)
        self.add_object(self.monster, Position(7, 7))
        hero.update_position(self.objects[PARTY].position)
        hero.ref(self.objects[PARTY])
        print(hero.position)


class Map6(WorldMap):
    def __init__(self):
        WorldMap.__init__(self, 'worldtest/map6.map',
                          LOWER_TILESET,
                          UPPER_TILESET)

    def initialize(self, local_state, global_state):
        self.add_area(RelativeTeleportArea(y_offset=-8, map_id=4), RectangleArea((8, 9), (8, 9)))
        self.add_area(RelativeTeleportArea(x_offset=-8, map_id=7), RectangleArea((9, 4), (9, 5)))
        self.add_object(SavePoint(self), Position(4, 4))
        hero.update_position(self.objects[PARTY].position)
        hero.ref(self.objects[PARTY])
        print(hero.position)


class Map7(WorldMap):
    def __init__(self):
        WorldMap.__init__(self, 'worldtest/map7.map',
                          LOWER_TILESET,
                          UPPER_TILESET)

    def initialize(self, local_state, global_state):
        self.add_area(RelativeTeleportArea(x_offset=+8, map_id=6), RectangleArea((0, 4), (0, 5)))

        self.monster = SmartMonster(self)
        self.add_object(self.monster, Position(5, 4))
        hero.update_position(self.objects[PARTY].position)
        hero.ref(self.objects[PARTY])
        print(hero.position)