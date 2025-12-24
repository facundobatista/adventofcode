test_lines = """
987654321111111
811111111111119
234234234234278
818181911112111
"""
expected_test_result = 357

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
    total = 0
    for bank in lines:
        elements = list(bank)
        pos = max(range(len(elements) - 1), key=lambda i: elements[i])
        b1 = int(elements[pos])
        elements[:pos + 1] = []
        pos = max(range(len(elements)), key=lambda i: elements[i])
        b2 = int(elements.pop(pos))
        print("==== bs", b1, b2)
        total += b1 * 10 + b2
    return total
