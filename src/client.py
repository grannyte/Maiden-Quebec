import curses


def main(stdscr):
    stdscr.nodelay(1)
    curses.noecho()
    curses.cbreak()
    curses.endwin()
    curses.curs_set(False)
    stdscr.keypad(True)

    while True:
        if stdscr.getch() == ord('q'):
            break

if __name__ == '__main__':
    curses.wrapper(main)