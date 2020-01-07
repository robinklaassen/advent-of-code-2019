from day11.intcode_computer import IntcodeComputer
from day19.puzzle_input import DRONE_PROGRAM


def point_is_pulled(computer: IntcodeComputer, x: int, y: int) -> bool:
    computer.reset()
    computer.start()
    computer.pass_input(x)
    computer.pass_input(y)
    output = computer.read_output()
    assert len(output) == 1
    return bool(output[0])


def fit_square_from_point(computer: IntcodeComputer, x: int, y: int, size: int = 100) -> bool:
    attempted_points = [(x, y), (x + size - 1, y), (x, y + size - 1)]
    for ax, ay in attempted_points:
        if not point_is_pulled(computer, ax, ay):
            return False
    return True


def main():
    """
    From part 1 it looks like the borders of the tractor beam can be approximated by the functions:
    y = (49/47) * x
    y = (49/41) * x
    This means that dy is approx. equal to 0.153 * x

    In half of delta-y we need to fit the square of width 100, so delta-y needs to be 200.
    So x is approximately 1310.
    And the center of the tractor beam is approximately y = (49/44) * x
    So y for this x is 1459.
    Let's use this as an ansatz...
    """
    program = DRONE_PROGRAM.copy()
    computer = IntcodeComputer(program)

    # This fits, tested manually
    x = 1310
    y = 1459

    while True:
        attempted_points = [(x - 1, y - 1), (x - 1, y), (x, y - 1)]
        for ax, ay in attempted_points:
            fits = fit_square_from_point(computer, ax, ay)
            print(f"Square at {(ax, ay)} {'fits' if fits else 'does not fit'}")
            if fits:
                x, y = ax, ay
                break
        else:
            break

    print(f"Final fitting point is {(x, y)}")
    print(f"Submit value: {10000 * x + y}")


if __name__ == "__main__":
    main()
