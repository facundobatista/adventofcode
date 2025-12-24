import re
import sys

lines = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()

LIMITS = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

matrix = [list(line) for line in lines]
around = {}


def _store(x, y, rematch):
    print("======= st", x, y, rematch)
    if x < 0 or y < 0:
        return
    try:
        char = matrix[x][y]
    except IndexError:
        return
    print("========== c", char)
    if char == "*":
        around.setdefault((x, y), set()).add(rematch)

for idx, line in enumerate(lines):
    print("======= L", repr(line))
    matches = re.finditer(r"(\d+)", line)
    for rematch in matches:
        inipos, endpos = rematch.span()

        # around current line
        _store(idx, inipos - 1, rematch)
        _store(idx, endpos, rematch)

        # previous line
        for pos in range(inipos - 1, endpos + 1):
            _store(idx - 1, pos, rematch)

        # next line
        for pos in range(inipos - 1, endpos + 1):
            _store(idx + 1, pos, rematch)

print("======== around!")
total = 0
for pos, matches in around.items():
    if len(matches) == 2:
        print("======== x", matches)
    elif len(matches) > 2:
        print("============= WTFFFFFFFFFFF", pos, matches)
    else:
        continue
    n1 = int(matches.pop().group())
    n2 = int(matches.pop().group())
    total += n1 * n2

print("Total", total)
