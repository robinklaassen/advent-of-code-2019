from day2.part1 import process_intcode, PUZZLE_INPUT

for noun in range(100):
    for verb in range(100):
        input_code = PUZZLE_INPUT.copy()
        input_code[1] = noun
        input_code[2] = verb
        output_code = process_intcode(input_code)
        output_value = output_code[0]
        print(f"Noun {noun} and verb {verb} results in output {output_value}")
        if output_value == 19690720:
            print(f"Submit value {100 * noun + verb}")
            break
    else:
        continue
    break
