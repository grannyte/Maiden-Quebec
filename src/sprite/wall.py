__author__ = 'plperron'

from pygame.sprite import Sprite


class Wall(Sprite):
    def __init__(self, image, rect):
        Sprite.__init__(self)
        self.image = image
        self.rect = rect