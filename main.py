# -*- coding: utf-8 -*-


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Text-based game')
    parser.add_argument('-i', '--irrlicht',
                        help='Irrlicht manages graphics(Not implemented yet)',
                        action='store_true')
    parser.parse_args()


if __name__ == "__main__":
    main()