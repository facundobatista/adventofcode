import re
import sys

import numpy as np


lines = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""
should_result = 480

if len(sys.argv) != 2:
    print("test or real?")
    exit()
if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
    should_result = None
else:
    print("Bad arg")
    exit()

blocks = []
curblock = []
for line in lines:
    line = line.strip()
    if not line:
        blocks.append(curblock)
        curblock = []
    else:
        curblock.append(line)
blocks.append(curblock)
print("====== len(blocks)", len(blocks))


def process(block):
    l1, l2, l3 = block

    ax, ay = re.match(r"Button A: X\+(\d+), Y\+(\d+)", l1).groups()
    bx, by = re.match(r"Button B: X\+(\d+), Y\+(\d+)", l2).groups()
    px, py = re.match(r"Prize: X=(\d+), Y=(\d+)", l3).groups()
    print("========= data", ax, ay, bx, by, px, py)

    A = np.array([[int(ax), int(bx)], [int(ay), int(by)]])
    b = np.array([int(px), int(py)])
    butA, butB = np.linalg.solve(A, b)
    print("========== solve!!", butA, butB)

    # floats, but check if really close to be integers
    if not round(butA, 10).is_integer():
        return 0
    if not round(butB, 10).is_integer():
        return 0
    if butA <= 0 or butB <= 0:
        raise ValueError("negativo?")

    butA = int(round(butA, 10))
    butB = int(round(butB, 10))
    return butA * 3 + butB


total = 0
for block in blocks:
    print("===== block", block)
    cost = process(block)
    print("======== cost", cost)
    total += cost


print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
