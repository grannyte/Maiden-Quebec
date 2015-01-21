__author__ = 'granyte'
from tile import Tile


class Spike(Tile):
    def __init__(self, x, y, spritesheet):
        Tile.__init__(self, x, y, spritesheet)
        rect = (3*32, 3*32, 32, 32)
        self.image = self._spritesheet.image_at(rect)

    def collide(self, p, xvel, yvel):
        if xvel > 0:
            p.rect.right = (self.rect.left-32)
        if xvel < 0:
            p.rect.left = (self.rect.right+32)
        if yvel > 0:
            p.rect.bottom = (self.rect.top-32)
        if yvel < 0:
            p.rect.top = (self.rect.bottom+32)