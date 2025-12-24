import sys

lines = """
0123
1234
8765
9876
"""

lines = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

# lines = """
# 12345
# """

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()


class SafeMap:
    def __init__(self):
        self.xmap = [list(map(int, line)) for line in lines]
        self.max_x = len(self.xmap[0])
        self.max_y = len(self.xmap)

    def __getitem__(self, coord):
        x, y = coord
        if (0 <= x < self.max_x) and (0 <= y < self.max_y):
            val = self.xmap[y][x]
        else:
            val = -1
        return val


xmap = SafeMap()


def walk(cx, cy, cval):
    print("========walk", (cx, cy), cval)

    should_next_val = cval + 1
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx = cx + dx
        ny = cy + dy
        nval = xmap[(nx, ny)]
        if nval == should_next_val:
            if should_next_val == 9:
                yield (nx, ny)
            else:
                yield from walk(nx, ny, nval)


# find trailheads
trailheads = []
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == "0":
            trailheads.append((x, y))

trailtops = set()
for x, y in trailheads:
    for top in walk(x, y, 0):
        trailtops.add((x, y, top))

print("======== trailtops", trailtops)
print("Total:", len(trailtops))
