# -*- coding: utf-8 -*-
from __future__ import print_function

from pygame import *


class Camera(object):
    def __init__(self, camera_func, width, height, win_width, win_height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)
        self.WIN_WIDTH = win_width
        self.HALF_WIDTH = int(win_width / 2)
        self.WIN_HEIGHT = win_height
        self.HALF_HEIGHT = int(win_height / 2)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


class SimpleCamera(Camera):
    def __init__(self, width, height, win_width, win_height):
        Camera.__init__(self, self._simple_camera, width, height,  win_width, win_height)

    def _simple_camera(self, camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        return Rect(-l + self.HALF_WIDTH, -t + self.HALF_HEIGHT, w, h)


class ComplexCamera(Camera):
    def __init__(self, width, height, win_width, win_height):
        Camera.__init__(self, self._complex_camera, width, height, win_width, win_height)

    def _complex_camera(self, camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t, _, _ = -l + self.HALF_WIDTH, -t + self.HALF_HEIGHT, w, h

        l = min(0, l)                           # stop scrolling at the left edge
        l = max(-(camera.width-self.WIN_WIDTH), l)   # stop scrolling at the right edge
        t = max(-(camera.height-self.WIN_HEIGHT), t)  # stop scrolling at the bottom
        t = min(0, t)                           # stop scrolling at the top
        return Rect(l, t, w, h)