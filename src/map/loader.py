# -*- coding: utf-8 -*-

class Map:
    grid = None

    def __init__(self, filename):
        self.grid = [list(line[:-1]) for line in open(filename)]

    def getNumberOfRows(self):
        return len(self.grid)

    def getNumberOfColumns(self):
        return len(self.grid[0])

    def getElement(self,x,y):
        return self.grid[x][y]

    def getPositionElement(self,element):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if(self.grid[row][col] == element):
                    return row, col

    def __str__(self):
        return ''.join(str(item) for line in self.grid for item in line)
