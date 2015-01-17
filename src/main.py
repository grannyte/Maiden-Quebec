# -*- coding: utf-8 -*-

import os
import sys
import argparse
from map.loader import Map

SCREEN_SIZE_ROW = 16
SCREEN_SIZE_COL = 60
SCREEN_CENTER_ROW = 8
SCREEN_CENTER_COL = 30
MAP_LIST = [ 'level00.map',
             'test2.map']

def main():
    parser = argparse.ArgumentParser(description='Text-based game')
    parser.add_argument('-i', '--irrlicht',
                        help='Irrlicht manages graphics(Not implemented yet)',
                        action='store_true')
    parser.parse_args()

    try:
        launch()
    except ExceptionGameComplete as e:
        print(e)

def launch():
    current_map = 0
    map_complete = True

    while(map_complete):
        try:
            map = Map(MAP_LIST[current_map])
        except IndexError as e:
            raise ExceptionGameComplete('Congratulations! Game complete!')

        heroe_pos_row, heroe_pos_col = map.getPositionElement('H')
        exit_pos_row, exit_pos_col = map.getPositionElement('E')
        map_complete = False

        command = ''
        while(command != 'q' and map_complete is False):
            clear_screen()

            first_map_row = SCREEN_CENTER_ROW - heroe_pos_row
            first_map_col = SCREEN_CENTER_COL - heroe_pos_col
            last_map_row = first_map_row + map.getNumberOfRows() - 1
            last_map_col = first_map_col + map.getNumberOfColumns() - 1

            for screen_row in range(SCREEN_SIZE_ROW):
                for screen_col in range(SCREEN_SIZE_COL):
                    map_row = screen_row - first_map_row
                    map_col = screen_col - first_map_col
                    if(map_row == heroe_pos_row and map_col == heroe_pos_col):
                        print('H',end="")
                    elif(screen_row >= first_map_row and screen_col >= first_map_col and
                            screen_row <= last_map_row and screen_col <= last_map_col):
                        element = map.getElement(map_row,map_col)
                        if(element != 'H'):
                            print(element, end="")
                        else:
                            print(' ', end="")
                    else:
                        print('.', end="")
                print('')

            # TODO: REAL MOVEMENT IMPLANTATION
            command = read_command()
            if(command == 's' and map.getElement(heroe_pos_row + 1,heroe_pos_col) != '#'):
                heroe_pos_row = heroe_pos_row + 1
            elif(command == 'w' and map.getElement(heroe_pos_row - 1,heroe_pos_col) != '#'):
                heroe_pos_row = heroe_pos_row - 1
            elif(command == 'a' and map.getElement(heroe_pos_row,heroe_pos_col - 1) != '#'):
                heroe_pos_col = heroe_pos_col - 1
            elif(command == 'd' and map.getElement(heroe_pos_row,heroe_pos_col + 1) != '#'):
                heroe_pos_col = heroe_pos_col + 1

            if(heroe_pos_row == exit_pos_row and heroe_pos_col == exit_pos_col):
                map_complete = True
                current_map += 1

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def read_command():
    return sys.stdin.read(1)

class ExceptionGameComplete(Exception):
    pass

if __name__ == "__main__":
    main()
