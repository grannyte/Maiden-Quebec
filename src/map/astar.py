import heapq
from loader import Map

def main():
    map = Map('test2.map')

    a = AStar(map)
    a.process()

class Cell(object):
    def __init__(self, x, y, reachable):
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

class AStar(object):
    def __init__(self, map):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.grid = map.grid
        self.grid_height = map.getNumberOfColumns()
        self.grid_width = map.getNumberOfRows()
        self.init_grid(map)

    def init_grid(self, map):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                current_element = map.getElement(x,y)
                if(current_element == '#'):
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))
                if(current_element == 'H'):
                    self.start = self.get_cell(x, y)
                elif(current_element == 'E'):
                    self.end = self.get_cell(x, y)

    def get_heuristic(self, cell):
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_cell(self, x, y):
        return self.cells[x * self.grid_height + y]

    def get_adjacent_cells(self, cell):
        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells

    def update_cell(self, adj, cell):
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def process(self):
        found_path = False

        # add cell to heap queue
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # pop cell from heap queue
            f, cell = heapq.heappop(self.opened)
            print(cell.x, " ", cell.y, " ", cell.f)

            # add cell to closed list
            self.closed.add(cell)

            # if end cell, display found path
            if cell is self.end:
                self.display_path()
                found_path = True
                break

            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is better than the one previously found for this adj cell.
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))

        if(not found_path):
            print("No path found.")

    def display_path(self):
        cell = self.end
        print("path: cell: ",cell.x,", ", cell.y)
        while cell.parent is not self.start:
            cell = cell.parent
            print("path: cell: ",cell.x,", ", cell.y)
        cell = self.start
        print("path: cell: ",cell.x,", ", cell.y)

if __name__ == "__main__":
    main()
