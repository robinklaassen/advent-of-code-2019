from day16.fft import fft, number_to_digits
from day16.puzzle_input import INPUT_NUMBER


def main():
    digits = number_to_digits(INPUT_NUMBER)
    output = fft(digits, 100)
    print(f"Submit value: {output[0:8]}")


if __name__ == "__main__":
    main()
