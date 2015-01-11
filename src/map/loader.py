# -*- coding: utf-8 -*-

class Map:
    map = None

    def __init__(self, filename):
        self.map = [list(line) for line in open(filename)]    

    def __str__(self):
        return ''.join(str(item) for line in self.map for item in line)
     
