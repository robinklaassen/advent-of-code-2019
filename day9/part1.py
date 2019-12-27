from day9.intcode_computer import IntcodeComputer
from day9.puzzle_input import BOOST_PROGRAM


def main():
    program = IntcodeComputer(BOOST_PROGRAM, memory_size=10240)
    program.start()
    program.pass_input(1)  # test mode
    print(program.read_output())


if __name__ == "__main__":
    main()
