test_lines = """
987654321111111
811111111111119
234234234234278
818181911112111
"""
expected_test_result = 3121910778619


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
    seqlen = 12
    for bank in lines:
        elements = list(bank)

        digits = []
        for limit in reversed(range(seqlen)):
            pos = max(range(len(elements) - limit), key=lambda i: elements[i])
            bank = elements[pos]
            digits.append(bank)
            elements[:pos + 1] = []
        print("==== bs", digits)
        total += int("".join(digits))
    return total
