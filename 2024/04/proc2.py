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


def trace(x, y):
    print("====== orig", x, y, xmap[(x, y)])

    #   coords for star
    #
    #   1 4
    #    A
    #   2 3
    coords = [
        (x - 1, y - 1),
        (x - 1, y + 1),
        (x + 1, y + 1),
        (x + 1, y - 1),
    ]

    # possibilities in the positions of the star ^
    should_all = [
        "MMSS",
        "SSMM",
        "SMMS",
        "MSSM",
    ]
    print("======= estrella:", [xmap[pos] for pos in coords])
    for should in should_all:
        if all(char == xmap[pos] for char, pos in zip(should, coords)):
            print("======= yes")
            return 1

    print("======= no")
    return 0


total = 0
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == "A":
            total += trace(x, y)

print("Total:", total)
