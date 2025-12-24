import sys

lines = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()


class SafeMap:
    def __init__(self):
        self.xmap = [list(line) for line in lines]
        self.max_x = len(self.xmap[0])
        self.max_y = len(self.xmap)

    def __getitem__(self, coord):
        x, y = coord
        if (0 <= x < self.max_x) and (0 <= y < self.max_y):
            val = self.xmap[y][x]
        else:
            val = None
        return val


xmap = SafeMap()


def validate(positions):
    for should, pos in zip("MAS", positions):
        if should != xmap[pos]:
            return 0
    return 1


def trace(x, y):
    print("====== orig", x, y, xmap[(x, y)])
    tot = 0
    tot += validate([(x + 0, y - 1), (x + 0, y - 2), (x + 0, y - 3)])  # 0:00
    tot += validate([(x + 1, y - 1), (x + 2, y - 2), (x + 3, y - 3)])  # 1:30
    tot += validate([(x + 1, y - 0), (x + 2, y - 0), (x + 3, y - 0)])  # 3:00
    tot += validate([(x + 1, y + 1), (x + 2, y + 2), (x + 3, y + 3)])  # 4:30
    tot += validate([(x + 0, y + 1), (x + 0, y + 2), (x + 0, y + 3)])  # 6:00
    tot += validate([(x - 1, y + 1), (x - 2, y + 2), (x - 3, y + 3)])  # 7:30
    tot += validate([(x - 1, y + 0), (x - 2, y + 0), (x - 3, y + 0)])  # 9:00
    tot += validate([(x - 1, y - 1), (x - 2, y - 2), (x - 3, y - 3)])  # 10:30
    return tot


total = 0
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == "X":
            total += trace(x, y)

print("Total:", total)
