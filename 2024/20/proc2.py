import sys
from collections import Counter

lines = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""
should_result = Counter({
    50: 32,
    52: 31,
    54: 29,
    56: 39,
    58: 25,
    60: 23,
    62: 20,
    64: 19,
    66: 12,
    68: 14,
    70: 12,
    72: 22,
    74: 4,
    76: 3,
})
save_limit = 50  # need to save this picoseconds or more
max_cheat_length = 20

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
    should_result = None
    save_limit = 100  # need to save this picoseconds or more
else:
    print("Bad arg")
    exit()


class SafeMap:

    # deltas
    DELTA_RIGHT = (1, 0)
    DELTA_LEFT = (-1, 0)
    DELTA_UP = (0, -1)
    DELTA_DOWN = (0, 1)
    ALL_DELTAS = [DELTA_DOWN, DELTA_RIGHT, DELTA_UP, DELTA_LEFT]
    _MARK = object()

    def __init__(self, lines, out_of_map=_MARK):
        self.xmap = [list(line) for line in lines]
        self.max_x = len(self.xmap[0])
        self.max_y = len(self.xmap)
        if out_of_map is self._MARK:
            def _f():
                raise ValueError("out of map")
            self.out_of_map = _f
        else:
            self.out_of_map = lambda: out_of_map

    def __getitem__(self, coord):
        x, y = coord
        if (0 <= x < self.max_x) and (0 <= y < self.max_y):
            val = self.xmap[y][x]
        else:
            val = self.out_of_map()

        return val

    def __setitem__(self, coord, value):
        x, y = coord
        if (0 <= x < self.max_x) and (0 <= y < self.max_y):
            self.xmap[y][x] = value
        else:
            raise ValueError("out of map")

    def switch(self, coord, delta):
        """Switch the element from the coordinate with the coordinate + delta."""
        x1, y1 = coord
        dx, dy = delta
        x2 = x1 + dx
        y2 = y1 + dy
        self.xmap[y1][x1], self.xmap[y2][x2] = self.xmap[y2][x2], self.xmap[y1][x1]
        return (x2, y2)

    def show(self):
        """Show the map."""
        width = len(self.xmap[0])
        print("-" * width)
        for row in self.xmap:
            print("".join(item for item in row))
        print("-" * width)

    def find(self, to_find):
        """Return the first ocurrence of item."""
        for y, row in enumerate(self.xmap):
            for x, item in enumerate(row):
                if item == to_find:
                    return x, y
        raise ValueError("Couldn't find " + repr(to_find))


# map constants
TILE_OK = "."
WALL = "#"
START = "S"
END = "E"


# delta of possible next position, and info for the movement
EXPLORATION = [
    SafeMap.DELTA_LEFT,
    SafeMap.DELTA_DOWN,
    SafeMap.DELTA_RIGHT,
    SafeMap.DELTA_UP,
]


def paint_walk(xmap):

    start_x, start_y = xmap.find(START)
    end_x, end_y = xmap.find(END)

    cur_x, cur_y, cur_len = start_x, start_y, 0
    positions = []

    while True:
        xmap[(cur_x, cur_y)] = cur_len
        positions.append((cur_x, cur_y))

        for dx, dy in EXPLORATION:
            new_x = cur_x + dx
            new_y = cur_y + dy
            new_len = cur_len + 1

            if new_x == end_x and new_y == end_y:
                # this is the end, beautiful friend, this is the end, my only friend, the end
                xmap[(new_x, new_y)] = new_len
                positions.append((new_x, new_y))
                return positions

            new_coords = (new_x, new_y)
            new_tile = xmap[new_coords]

            if new_tile == TILE_OK:
                cur_x, cur_y, cur_len = new_x, new_y, new_len
                break


xmap = SafeMap(lines)
xmap.show()
end_coords = xmap.find(END)

positions = paint_walk(xmap)

# this is to understand numbering
width = len(xmap.xmap[0])
print("---" * width)
for row in xmap.xmap:
    print("".join(f"{item:3d}" if isinstance(item, int) else item * 3 for item in row))
print("---" * width)

max_number = len(positions) - 1
counter = Counter()
for ini_number in range(max_number + 1):
    for end_number in range(ini_number + save_limit, max_number + 1):
        # print("==== num from to", ini_number, end_number)
        x1, y1 = positions[ini_number]
        x2, y2 = positions[end_number]
        distance = abs(x1 - x2) + abs(y1 - y2)
        if distance > max_cheat_length:
            continue
        # print("==== dist", distance)
        cheat = end_number - ini_number - distance
        if cheat >= save_limit:
            counter[cheat] += 1

for cheat, quant in counter.most_common():
    print(cheat, quant)

total = sum(counter.values())
print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
