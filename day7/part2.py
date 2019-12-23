import itertools
from typing import Tuple, List

from day7.intcode_program_2 import IntcodeProgram2, ProgramState
from day7.puzzle_input import AMPLIFIER_CONTROLLER_SOFTWARE


def run_amplifiers(program: List[int], phases: Tuple[int, int, int, int, int]) -> int:
    # Set up 5 amplifier programs in a list
    amps: List[IntcodeProgram2] = []
    for _ in range(5):
        amps.append(IntcodeProgram2(program))

    # Start each program and give it a phase
    for amp in amps:
        amp.start()
        amp_index = amps.index(amp)
        amp.pass_input(phases[amp_index])

    # Pass 0 to the first amp once
    amps[0].pass_input(0)

    # Loop until halts
    for i in range(1_000_000):
        ix_current = i % 5  # index of amp to get input from
        ix_next = (i + 1) % 5  # index of amp to pass input to

        value = amps[ix_current].read_output()

        # Stop iterating if all amps are halted
        if all(map(lambda a: a.state == ProgramState.HALTED, amps)):
            break

        amps[ix_next].pass_input(value)
    else:
        raise Exception("Amplifier loop exceeded max iterations")

    return value


def find_max_output(program: List[int]) -> int:
    attempts = itertools.permutations(range(5, 10), 5)
    outputs = []
    for attempted_phases in attempts:
        outputs.append(run_amplifiers(program, attempted_phases))  # type: ignore
    return max(outputs)


def main():
    # No assertions, this just magically worked at once!
    output = find_max_output(AMPLIFIER_CONTROLLER_SOFTWARE)
    print(f"Submit value: {output}")


if __name__ == "__main__":
    main()
