__author__ = 'granyte'
from tile import Tile


class Spike(Tile):
    def __init__(self, x, y, spritesheet):
        Tile.__init__(self, x, y, spritesheet)
        rect = (0, 0, 64, 64)
        self.image = self._spritesheet.image_at(rect)

    def collide(self, p, xvel, yvel):
        if xvel > 0:
            p.rect.right = (self.rect.left-64)
        if xvel < 0:
            p.rect.left = (self.rect.right+64)
        if yvel > 0:
            p.rect.bottom = (self.rect.top-64)
        if yvel < 0:
            p.rect.top = (self.rect.bottom+64)