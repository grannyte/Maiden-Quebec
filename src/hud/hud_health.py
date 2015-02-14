# -*- coding: utf-8 -*-
from __future__ import print_function

from src.hud.status_hud import StatusHud


class HudHealth(StatusHud):
    def __init__(self):
        StatusHud.__init__(self)
        self._label = self.hud_font.render("HP", 1, (255, 0, 0))
        self._color = (255, 0, 0)
        self._rect = (32, 9, 128, 8)
        self._rect_width = 128 - 32

    def update(self, current_hp, max_hp):
        pourcent_hp = self._rect_width * current_hp / max_hp
        rect = (self._rect[0], self._rect[1], pourcent_hp, self._rect[3])
        return {'label': self._label, 'at': (2, 4), 'hp': rect, 'color': self._color}
