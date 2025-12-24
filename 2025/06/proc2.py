import functools
import operator

test_lines = """
123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
"""
expected_test_result = 3263827



def run(lines):
    # spaces are important, complete to the longest
    longest = max(len(line) for line in lines)
    lines = [line + (" " * (longest - len(line))) for line in lines]
    print("=========== lines", lines)

    # traverse from right to left columns
    sequence = list(reversed(list(zip(*lines))))

    numbers = []
    total = 0
    for seq in sequence:
        print("==== seq", seq)
        *digits, op = seq
        digits = "".join(digits).strip()
        if not digits:
            # empty column
            continue

        num = int(digits)
        numbers.append(num)

        op = op.strip()
        if op:
            print("======== op!!", (op, numbers))
            if op == "+":
                partial = sum(numbers)
            elif op == "*":
                partial = functools.reduce(operator.mul, numbers)
            else:
                raise ValueError("bad op")
            total += partial
            numbers = []

    return total
