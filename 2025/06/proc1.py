import functools
import operator

test_lines = """
123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
"""
expected_test_result = 4277556


def _process_lines(lines):
    lines = [x.split() for x in lines]
    return list(zip(*lines))


def run(lines):
    operations = _process_lines(lines)
    total = 0
    for operation in operations:
        print("====== op", operation)
        *nums, op = operation
        nums = [int(x) for x in nums]

        if op == "+":
            partial = sum(nums)
        elif op == "*":
            partial = functools.reduce(operator.mul, nums)
        else:
            raise ValueError("bad op")
        total += partial

    return total
