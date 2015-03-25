from librpg.world import World
from librpg.party import Character

from worldtest.mymaps import *

from worldtest.lsystemmap import *

def char_factory(name):
    return Character('Andy', charset_path('player.png'))


class MyWorld(World):
    def __init__(self, save_file=None):
        maps = {1: Map1, 2: Map2, 3: Map3, 4: Map4, 5: Map5, 6: Map6, 7: Map7, 8: LSystemMap}

        World.__init__(self, maps=maps, character_factory=char_factory)
        if save_file is None:
            self.initial_state(map=1, position=Position(5, 4), chars=['Andy'])
        else:
            self.load_state(state_file=save_file)

    def custom_gameover(self):
        print 'Fin du jeu.'
