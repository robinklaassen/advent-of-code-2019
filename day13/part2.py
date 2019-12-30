import curses
from enum import Enum, auto
from typing import List, Optional, Tuple

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


class PlayMode(Enum):
    MANUAL = auto()
    AUTO = auto()


def parse_output(output: List[int],
                 game_window,
                 score_window) -> Tuple[Optional[int], Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
    score = None
    paddle_pos = None
    ball_pos = None

    for triplet in np.array_split(output, len(output) / 3):
        x, y, val = triplet
        if x == -1 and y == 0:  # val is the game score
            score = val
            score_window.clear()
            score_window.addstr(0, 0, str(score))
        else:  # val is a character on the screen
            if val == 3:
                paddle_pos = (x, y)
            elif val == 4:
                ball_pos = (x, y)
            game_window.addch(y, x, ARCADE_CHARS[val])

    game_window.refresh()
    score_window.refresh()
    return score, paddle_pos, ball_pos


def run_terminal(screen):
    play_mode = PlayMode.AUTO

    # Set up screen
    screen_max_y, screen_max_x = screen.getmaxyx()
    curses.curs_set(0)  # disables blinking cursor
    curses.cbreak()  # do not buffer character input
    curses.noecho()  # do not directly echo input
    # curses.halfdelay(0)  # arg = delay for each getch() in tenths of a second

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
    input_window.nodelay(True)

    _, paddle_pos, ball_pos = parse_output(output, game_window, score_window)
    score = 0
    frame_delay = 0 if play_mode == PlayMode.AUTO else 500

    while not computer.is_halted():

        c = input_window.getch()  # returns -1 if no key was pressed in nodelay mode

        if c == 27:  # esc
            print("Escaping...")
            break

        if c == 32:  # spacebar
            frame_delay = 50 if frame_delay == 500 else 500

        if play_mode == PlayMode.MANUAL:
            input_ = INPUT_MAP.get(c, 0)
        elif play_mode == PlayMode.AUTO:
            if paddle_pos[0] > ball_pos[0]:
                input_ = -1
            elif paddle_pos[0] < ball_pos[0]:
                input_ = 1
            else:
                input_ = 0
        else:
            input_ = 0

        computer.pass_input(input_)
        output = computer.read_output()
        things = parse_output(output, game_window, score_window)
        score = things[0] or score
        paddle_pos = things[1] or paddle_pos
        ball_pos = things[2] or ball_pos

        curses.napms(frame_delay)

    print(f"Game exited with final score: {score}")


def main():
    print("Starting game...")
    curses.wrapper(run_terminal)


if __name__ == "__main__":
    main()
