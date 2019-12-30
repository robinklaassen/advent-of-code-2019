import curses
from typing import List, Optional

import numpy as np

from day11.intcode_computer import IntcodeComputer
from day13.puzzle_input import GAME_PROGRAM

ARCADE_CHARS = {
    0: ' ',
    1: 'X',
    2: '#',
    3: '=',
    4: 'O',
}

INPUT_MAP = {
    curses.KEY_LEFT: -1,
    curses.KEY_RIGHT: 1,
}


def draw_output_and_return_score(output: List[int], game_window, score_window) -> Optional[int]:
    score = None
    for triplet in np.array_split(output, len(output) / 3):
        x, y, val = triplet
        if x == -1 and y == 0:  # val is the game score
            score = val
            score_window.clear()
            score_window.addstr(0, 0, str(score))
        else:  # val is a character on the screen
            game_window.addch(y, x, ARCADE_CHARS[val])

    game_window.refresh()
    score_window.refresh()
    return score


def run_terminal(screen):
    # Set up screen
    screen_max_y, screen_max_x = screen.getmaxyx()
    curses.curs_set(0)  # disables blinking cursor
    curses.cbreak()  # do not buffer character input
    curses.noecho()  # do not directly echo input
    curses.halfdelay(2)  # arg = delay for each getch() in tenths of a second

    # Change program to play for free
    program = GAME_PROGRAM.copy()
    program[0] = 2

    # Start the program and create initial output
    computer = IntcodeComputer(program, memory_size=10240)
    computer.start()
    output = computer.read_output()
    x_size = max(output[::3]) + 1
    y_size = max(output[1::3]) + 1

    if x_size > screen_max_x + 13 or y_size > screen_max_y:
        raise Exception("Screen too small!")

    # Set up game windows
    # x + 1 because otherwise cursor falls off screen after last char on line
    game_window = curses.newwin(y_size, x_size + 1, 0, 0)
    score_window = curses.newwin(1, 10, 0, x_size + 3)
    input_window = curses.newwin(1, 1, 3, x_size + 3)
    input_window.keypad(True)

    draw_output_and_return_score(output, game_window, score_window)
    score = 0

    while not computer.is_halted():

        c = input_window.getch()  # returns -1 if no key was pressed in nodelay mode
        input_ = INPUT_MAP.get(c, 0)

        computer.pass_input(input_)
        output = computer.read_output()
        new_score = draw_output_and_return_score(output, game_window, score_window)
        score = new_score or score

        curses.napms(300)

    print(f"Finished the game with final score: {score}")


def main():
    print("Starting arcade game...")
    curses.wrapper(run_terminal)


if __name__ == "__main__":
    main()
