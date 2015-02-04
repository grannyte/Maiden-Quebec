import heapq

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
    def process(self):
        self.opened = []
        self.closed = set()

        # add start cell to heap queue
        heapq.heapify(self.opened)
        heapq.heappush(self.opened, (self.start.f, self.start))

        while len(self.opened):
            # pop cell from heap queue
            f, cell = heapq.heappop(self.opened)
            # add cell to closed list
            self.closed.add(cell)
            # if end cell, display found path
            if cell is self.end:
                self.path_found = True
                break
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is better than the one previously found for this adj cell.
                        if adj_cell.g > cell.g + self.get_heuristic_base_value():
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))

    def update_cell(self, adj, cell):
        adj.g = cell.g + self.get_heuristic_base_value()
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g


class Search(AStar):
    def __init__(self, grid):
        self.cells = []
        self.grid_def = {'start':'H', 'end':'E', 'wall':'#'}
        self.grid_height = len(grid[0])
        self.grid_width = len(grid)
        self.path_found = False
        self.init_grid(grid)

    def init_grid(self, grid):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                current_element = grid[x][y]
                if(current_element == self.grid_def['wall']):
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))
                if(current_element == self.grid_def['start']):
                    self.start = self.get_cell(x, y)
                elif(current_element == self.grid_def['end']):
                    self.end = self.get_cell(x, y)

    def get_heuristic(self, cell):
        return self.get_heuristic_base_value() * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_heuristic_base_value(self):
        return 10

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

    def display_path(self):
        if(self.path_found):
            cell = self.end
            print("path: cell: ",cell.x,", ", cell.y)
            while cell.parent is not self.start:
                cell = cell.parent
                print("path: cell: ",cell.x,", ", cell.y)
            cell = self.start
            print("path: cell: ",cell.x,", ", cell.y)

    def display_path_as_grid(self):
        path = self.get_path()
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                cell = self.get_cell(x,y)
                if((x,y) in path):
                    print("o", end="")
                elif(cell.reachable):
                    print(" ", end="")
                else:
                    print("#", end="")
            print()

    def get_path(self):
        cells = []
        if(self.path_found):
            cell = self.end
            cells.append((cell.x, cell.y))
            while cell.parent is not self.start:
                cell = cell.parent
                cells.append((cell.x, cell.y))
            cell = self.start
            cells.append((cell.x, cell.y))
        return cells

