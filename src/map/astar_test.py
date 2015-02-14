from map import Map
from astar import *

def main():
    map = Map('test10.map')
    map.print_as_grid()
    world = World(map.grid)
    initial_state = State(Cell(1,1,True))
    goal = Goal(Cell(13,39,True))
    heuristic = Heuristic()
    astar = AStar(world, initial_state, goal, heuristic)

    current_state = astar.final_state
    if(current_state != None):
        print("found")
        while(current_state != None):
            print("Cell: " + str(current_state.cell.x) + "," + str(current_state.cell.y))
            current_state = current_state.parent
    else:
        print("not found")


if __name__ == "__main__":
    main()
