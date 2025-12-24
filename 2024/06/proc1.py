import sys
from itertools import cycle

lines = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()


class ExtraMap:
    OK, BLOCK, OUT = 0, 1, 2

    def __init__(self):
        self.map = [list(line) for line in lines]
        self.max_x = len(self.map[0])
        self.max_y = len(self.map)

        self.blocks = set()
        for y, row in enumerate(self.map):
            for x, char in enumerate(row):
                if char == "#":
                    self.blocks.add((x, y))

    def __getitem__(self, coord):
        x, y = coord
        if (0 <= x < self.max_x) and (0 <= y < self.max_y):
            if (x, y) in self.blocks:
                val = self.BLOCK
            else:
                val = self.OK
        else:
            val = self.OUT
        return val


xmap = ExtraMap()


def get_guard_initial_pos():
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "^":
                return (x, y)
    raise ValueError("Guard not found")


# deltas that the guard can walk
directions = cycle([
    (0, -1),
    (+1, 0),
    (0, +1),
    (-1, 0),
])


current_pos = get_guard_initial_pos()
direction = next(directions)
walked_positions = set()
while True:
    walked_positions.add(current_pos)
    print("======== walk", current_pos, direction)
    c_x, c_y = current_pos
    d_x, d_y = direction
    next_pos = (c_x + d_x, c_y + d_y)
    peek = xmap[next_pos]
    print("=========== peek", peek)
    if peek == ExtraMap.OUT:
        # we're done!
        break

    if peek == ExtraMap.BLOCK:
        # blocked! turn and try new direction from current position
        direction = next(directions)
    elif peek == ExtraMap.OK:
        # free to go! move
        current_pos = next_pos
    else:
        raise ValueError("Bad map block")


total = len(walked_positions)
print("Total:", total)
