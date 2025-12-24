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


def walk(cx, cy, cval, cseq):
    print("========walk", (cx, cy), cval, cseq)

    should_next_val = cval + 1
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx = cx + dx
        ny = cy + dy
        nval = xmap[(nx, ny)]
        if nval == should_next_val:
            nseq = cseq + ((nx, ny), )
            if should_next_val == 9:
                yield nseq
            else:
                yield from walk(nx, ny, nval, nseq)


# find trailheads
trailheads = []
for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == "0":
            trailheads.append((x, y))

trails = set()
for x, y in trailheads:
    for trail in walk(x, y, 0, ((x, y)),):
        print("============= trail!", trail)
        trails.add(trail)

print("Total:", len(trails))
