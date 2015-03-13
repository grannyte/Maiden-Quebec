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

SAVE_FILE = 'save'
LOWER_TILESET = (tileset_path('city_lower.png'),
                 tileset_path('city_lower.bnd'))
UPPER_TILESET = [(tileset_path('world_upper.png'),
                  tileset_path('world_upper.bnd'))]
HP_INITIAL = 100
HAUT_TOUR = 12
BAS_TOUR = 22

class SavePoint(ScenarioMapObject):
    def __init__(self, map):
        ScenarioMapObject.__init__(self, map, 0, 1)
        self.map = map

    def activate(self, party_avatar, direction):
        self.map.schedule_message(MessageDialog(u'Votre partie se sauvegarge dans %s.' % SAVE_FILE, block_movement=True))
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
        if(self.hp <= 0):
            print(u'Le monstre est mort.')
            self.destroy()

    def collide_with_party(self, party_avatar, direction):
        print('defense')

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
        if(self.hp <= 0):
            print(u'Le monstre est mort.')
            self.destroy()

    def collide_with_party(self, party_avatar, direction):
        print('defense')

    def update(self):
        pass


class ProtectedArea(MapArea):
    def __init__(self, map, movements):
        self.map = map
        self.movements = movements

    def party_entered(self, party_avatar, position):
        if(self.map.guard.position.x != 2):
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
        self.add_object(MessagePoint(self,HAUT_TOUR,u'Vieil homme dans la tour: Vous aviez bu trop de Maiden-Quebec et vous avez coulé votre navire.  Les vagues vous ont ramené sur le rivage, comptez vous chanceux d\'être en vie! Vous devriez retourner à la maison maintenant...'), Position(3, 3))
        self.add_object(MessagePoint(self,BAS_TOUR,u'Vieil homme dans la tour: Vous aviez bu trop de Maiden-Quebec et vous avez coulé votre navire.  Les vagues vous ont ramené sur le rivage, comptez vous chanceux d\'être en vie! Vous devriez retourner à la maison maintenant...'), Position(3, 4))


class Map2(WorldMap):
    def __init__(self):
        WorldMap.__init__(self, 'worldtest/map2.map',
                          LOWER_TILESET,
                          UPPER_TILESET)

    def initialize(self, local_state, global_state):
        self.add_area(RelativeTeleportArea(x_offset=+8, map_id=1), RectangleArea((0, 2), (0, 7)))
        self.add_area(RelativeTeleportArea(x_offset=-8, map_id=3), RectangleArea((9, 2), (9, 7)))
        self.add_area(RelativeTeleportArea(y_offset=+8, map_id=4), RectangleArea((4, 0), (5, 0)))
        self.add_object(SavePoint(self), Position(5, 2))


class Map3(WorldMap):
    def __init__(self):
        WorldMap.__init__(self, 'worldtest/map3.map',
                          LOWER_TILESET,
                          UPPER_TILESET)

    def initialize(self, local_state, global_state):
        self.add_object(GameOverBarrel(self), Position(9, 3))
        self.add_object(GameOverBarrel(self), Position(9, 7))
        self.add_object(Monster(), Position(8,5))
        self.add_area(RelativeTeleportArea(x_offset=+8, map_id=2), RectangleArea((0, 3), (0, 6)))

        if local_state is not None:
            self.chest = Chest(local_state['chest_closed'])
        else:
            self.chest = Chest()
        self.add_object(self.chest, Position(9, 5))

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
        self.add_object(self.guard, Position(8,3))

        movements = [ForcedStep(LEFT) for _ in range(6)]
        self.add_area(ProtectedArea(self, movements), RectangleArea((1,5),(1,5)))

        self.add_object(MessagePoint(self,HAUT_TOUR,u'Sage de la tour: Bravo! Belle idée de venir ici!'), Position(1, 5))
        self.add_object(MessagePoint(self,BAS_TOUR,u'Sage de la tour: Bravo! Belle idée de venir ici!'), Position(1, 6))


class Map5(WorldMap):
    def __init__(self):
        WorldMap.__init__(self, 'worldtest/map5.map',
                          LOWER_TILESET,
                          UPPER_TILESET)

    def initialize(self, local_state, global_state):
        self.add_area(RelativeTeleportArea(x_offset=+8, map_id=4), RectangleArea((0, 4), (0, 5)))


class Map6(WorldMap):
    def __init__(self):
        WorldMap.__init__(self, 'worldtest/map6.map',
                          LOWER_TILESET,
                          UPPER_TILESET)

    def initialize(self, local_state, global_state):
        self.add_area(RelativeTeleportArea(y_offset=-8, map_id=4), RectangleArea((8, 9), (8, 9)))
        self.add_object(SavePoint(self), Position(4, 4))

