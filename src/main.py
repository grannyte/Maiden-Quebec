# -*- coding: utf-8 -*-


def main():
    """
    Point d'entré du programme.  Celui-ci valide que les arguments passés en paramètre
    sont conformes.
    """
    import argparse

    parser = argparse.ArgumentParser(description='Text-based game')
    parser.add_argument('-i', '--irrlicht',
                        help='Irrlicht manages graphics(Not implemented yet)',
                        action='store_true')
    parser.parse_args()


if __name__ == "__main__":
    main()