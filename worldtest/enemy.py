from __future__ import print_function

"Le module definit les ennemies posssible a rencontrer"


from librpg.mapobject import MapObject


class Enemy(MapObject):
    def __init__(self):
        MapObject.__init__(self, MapObject.OBSTACLE,
                           image_file='hulk.png')
        self.__next_action = []
        self.hp = 100


class Hero(Enemy):
    def __init__(self):
        self.hp = 100
        self.position = None

    def update_position(self, position):
        self.position = position


class Common(Enemy):
    pass


class Boss(Enemy):
    pass


__author__ = 'plperron'
