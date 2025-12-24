test_lines = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""
expected_test_result = 3

dial_start = 50
dial_size = 100


def _parse_lines(lines):
    rotations = []
    for line in lines:
        direction, digits = line[0], line[1:]
        quant = int(digits)
        if direction == "L":
            quant *= -1
        rotations.append(quant)
    return rotations


def run(lines):
    rotations = _parse_lines(lines)
    dial = dial_start
    count = 0
    for rot in rotations:
        dial += rot
        while dial < 0:
            dial += dial_size
        while dial >= dial_size:
            dial -= dial_size
        print("======= rot", rot, dial)
        if dial == 0:
            count += 1

    return count
