# -*- coding: utf-8 -*-

from map import loader as Loader
import argparse


def main():
    """
    Point d'entré du programme.  Celui-ci valide que les arguments passés en paramètre
    sont conformes.
    """

    parser = argparse.ArgumentParser(description='Text-based game')
    parser.add_argument('-i', '--irrlicht',
                        help='Irrlicht manages graphics(Not implemented yet)',
                        action='store_true')
    parser.parse_args()

    # Prochaines lignes a effacer au besoin
    map_from_file = Loader.Map('test2.map')
    print(map_from_file)


if __name__ == "__main__":
    main()