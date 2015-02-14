from abstract_astar import Action as AA_Action, Goal as AA_Goal, Heuristic as AA_Heuristic, State as AA_State, World as AA_World, AStar

class Cell(object):
    def __init__(self, x, y, reachable):
        self.reachable = reachable
        self.x = x
        self.y = y

    def __eq__(self, othercell):
        return self.x == othercell.x and self.y == othercell.y

class Action(AA_Action):
    def __init__(self, cost, cell):
        self.cost = cost
        self.cell = cell

class Goal(AA_Goal):
    def __init__(self, cell):
        self.cell = cell

    def is_reached(self, state):
        return self.cell == state.cell

class Heuristic(AA_Heuristic):
    def __init__(self):
        pass

    def estimate_cost_to_goal(self, state, goal):
        return 10 * (abs(goal.cell.x - state.cell.x) + abs(goal.cell.y - state.cell.y))

class State(AA_State):
    def __init__(self, cell):
        self.cell = cell
        self.parent = None
        self.action_since_parent = None
        self.f = 0
        self.g = 0
        self.h = 0

    def __eq__(self, otherstate):
        if(otherstate != None):
            return self.cell.x == otherstate.cell.x and self.cell.y == otherstate.cell.y
        else:
            return None

    def __lt__(self, otherstate):
        return self.f < otherstate.f

class World(AA_World):
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

    def getActions(self, state):
        actions = []
        if state.cell.x < self.grid_width-1 and self.get_cell(state.cell.x+1, state.cell.y).reachable == True:
            actions.append(Action(10,self.get_cell(state.cell.x+1, state.cell.y)))
        if state.cell.y > 0 and self.get_cell(state.cell.x, state.cell.y-1).reachable == True:
            actions.append(Action(10,self.get_cell(state.cell.x, state.cell.y-1)))
        if state.cell.x > 0 and self.get_cell(state.cell.x-1, state.cell.y).reachable == True:
            actions.append(Action(10,self.get_cell(state.cell.x-1, state.cell.y)))
        if state.cell.y < self.grid_height-1 and self.get_cell(state.cell.x, state.cell.y+1).reachable == True:
            actions.append(Action(10,self.get_cell(state.cell.x, state.cell.y+1)))
        return actions

    def execute(self, etat, action):
        return State(Cell(action.cell.x, action.cell.y, True))

    def get_cell(self, x, y):
        return self.cells[x * self.grid_height + y]

