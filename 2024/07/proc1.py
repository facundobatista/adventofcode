import sys
from itertools import product
from operator import add, mul

lines = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()


def solve(elements, operations, target):
    operations = list(operations)
    # print("====== all ops", operations)
    for sequence in operations:
        base = elements[0]
        for op, elem in zip(sequence, elements[1:]):
            if base > target:
                break
            # print("====== solv", base, op, elem)
            base = op(base, elem)
        if base == target:
            return True
    return False


def tryout(result, parts):
    print("====== try", result, parts)
    operations = product((add, mul), repeat=len(parts) - 1)
    ok = solve(parts, operations, result)
    print("========== ok?", ok)
    return ok


total = 0
for line in lines:
    result, parts = line.strip().split(":")
    result = int(result)
    parts = [int(x) for x in parts.split()]
    ok = tryout(result, parts)
    if ok:
        total += result

print("Total:", total)
