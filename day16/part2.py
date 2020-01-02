from day16.fft import number_to_digits, digits_to_number
from day16.puzzle_input import INPUT_NUMBER


def main():
    digits = number_to_digits(INPUT_NUMBER)
    msg_offset_digits = digits[0:7]
    msg_offset = int(digits_to_number(msg_offset_digits))
    digits = digits * 10000

    print(f"Total number of digits: {len(digits)}")
    print(f"Message offset: {msg_offset}")

    reduced_digits = digits[msg_offset:]
    print(f"Reduced number of digits: {len(reduced_digits)}")

    signal = reduced_digits.copy()

    for phase in range(100):

        new_signal = []
        for i in range(len(signal)):
            if i == 0:
                the_sum = sum(signal)
            else:
                the_sum = the_sum - signal[i-1]
            value = abs(the_sum) % 10
            new_signal.append(value)

        signal = new_signal.copy()
        print(f"Finished phase {phase}")

    message_digits = signal[0:8]
    message = digits_to_number(message_digits)
    print(f"Submit value: {message}")


if __name__ == "__main__":
    main()
