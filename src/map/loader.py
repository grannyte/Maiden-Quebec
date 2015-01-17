# -*- coding: utf-8 -*-

class Map:
    map = None

    def __init__(self, filename):
        self.map = [list(line[:-1]) for line in open(filename)]

    def getNumberOfRows(self):
        return len(self.map)

    def getNumberOfColumns(self):
        return len(self.map[0])

    def getElement(self,x,y):
        return self.map[x][y]

    def getPositionElement(self,element):
        for row in range(len(self.map)):
            for col in range(len(self.map[0])):
                if(self.map[row][col] == element):
                    return row, col

    def __str__(self):
        return ''.join(str(item) for line in self.map for item in line)

