import heapq

class Action(object):
    def __init__(self, cost):
        raise NotImplementedError('subclasses must override this method')

class Goal(object):
    def __init__(self):
        raise NotImplementedError('subclasses must override this method')

    def is_reached(self, state):
        raise NotImplementedError('subclasses must override this method')

class Heuristic(object):
    def __init__(self):
        raise NotImplementedError('subclasses must override this method')

    def estimate_cost_to_goal(self, state, goal):
        raise NotImplementedError('subclasses must override this method')

class State(object):
    def __init__(self, cell):
        raise NotImplementedError('subclasses must override this method')

class World(object):
    def __init__(self, grid):
        raise NotImplementedError('subclasses must override this method')

    def getActions(self, state):
        raise NotImplementedError('subclasses must override this method')

    def execute(self, etat, action):
        raise NotImplementedError('subclasses must override this method')

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
