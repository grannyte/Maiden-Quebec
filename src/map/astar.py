from map import Map
import heapq

def main():
    map = Map('test10.map')
    map.print_as_grid()
    world = World(map.grid)
    initial_state = State(Cell(1,1,True))
    goal = Goal(Cell(13,39,True))
    heuristic = Heuristic()
    astar = AStar(world, initial_state, goal, heuristic)

    final_state = astar.final_state
    if(final_state != None):
        print("found")
        while(final_state != None):
            print("Cell: " + str(final_state.cell.x) + "," + str(final_state.cell.y))
            final_state = final_state.parent
    else:
        print("not found")

class Cell(object):
    def __init__(self, x, y, reachable):
        self.reachable = reachable
        self.x = x
        self.y = y

    def __eq__(self, othercell):
        return self.x == othercell.x and self.y == othercell.y

class Action(object):
    def __init__(self, cost, cell):
        self.cost = cost
        self.cell = cell

class Goal(object):
    def __init__(self, cell):
        self.cell = cell

    def is_reached(self, state):
        return self.cell == state.cell

class Heuristic(object):
    def __init__(self):
        pass

    def estimate_cost_to_goal(self, state, goal):
        return 10 * (abs(goal.cell.x - state.cell.x) + abs(goal.cell.y - state.cell.y))

class State(object):
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

class World(object):
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


class AStar(object):
    def __init__(self, world, initialState, goal, heuristic):
        self.opened = []
        self.closed = []
        self.final_state = None

        # add the first state to the heap
        heapq.heapify(self.opened)
        heapq.heappush(self.opened, (initialState.f, initialState))

        while len(self.opened):
            # pop state from heap queue
            f, actual_state = heapq.heappop(self.opened)
            print("POP: " + str(actual_state.f) + " " + str(actual_state.cell.x) + " " + str(actual_state.cell.y))
            # add state to closed list
            self.closed.append(actual_state)

            # if goal is reached, stop
            if goal.is_reached(actual_state):
                self.final_state = actual_state
                break

            # get possible actions from current state
            possible_actions = world.getActions(actual_state)

            for action in possible_actions:
                next_state = world.execute(actual_state, action)
                next_state.action_since_parent = action
                next_state.g = actual_state.g + action.cost
                next_state.h = heuristic.estimate_cost_to_goal(next_state, goal)
                next_state.f = next_state.g + next_state.h
                next_state.parent = actual_state

                if(next_state not in self.closed):
                    if((next_state.f, next_state) not in self.opened):
                        heapq.heappush(self.opened, (next_state.f, next_state))


if __name__ == "__main__":
    main()
