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
    2: 14,
    4: 14,
    6: 2,
    8: 4,
    10: 2,
    12: 3,
    20: 1,
    36: 1,
    38: 1,
    40: 1,
    64: 1,
})

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
    should_result = None
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

    while True:
        xmap[(cur_x, cur_y)] = cur_len

        for dx, dy in EXPLORATION:
            new_x = cur_x + dx
            new_y = cur_y + dy
            new_len = cur_len + 1

            if new_x == end_x and new_y == end_y:
                # this is the end, beautiful friend, this is the end, my only friend, the end
                xmap[(new_x, new_y)] = new_len
                return

            new_coords = (new_x, new_y)
            new_tile = xmap[new_coords]

            if new_tile == TILE_OK:
                cur_x, cur_y, cur_len = new_x, new_y, new_len
                break


def search(xmap, cheat1, cheat2, end_coords):
    print("======= search", cheat1, cheat2, end_coords)
    if xmap[cheat2] == WALL:
        # cheat process must end in the hall
        return 0

    around1 = []
    around2 = []
    for cheat_tile, around in [(cheat1, around1), (cheat2, around2)]:
        for dx, dy in xmap.ALL_DELTAS:
            cx, cy = cheat_tile
            nx = cx + dx
            ny = cy + dy
            coords = (nx, ny)
            if coords == cheat1 or coords == cheat2:
                continue
            tile = xmap[coords]
            if tile == WALL:
                continue
            around.append(tile)
    print("=========== arounds", around1, around2)

    if cheat1 == end_coords:
        min_from_1 = min(around1, default=sys.maxsize)
        min_from_2 = min(around2, default=sys.maxsize)
        cheat = max(84 - min_from_1 - 1, 84 - min_from_2 - 2)
        print("=========== cheat (end1)", cheat)
    elif cheat2 == end_coords:
        min_from_1 = min(around1, default=sys.maxsize)
        min_from_2 = min(around2, default=sys.maxsize)
        cheat = max(84 - min_from_2 - 1, 84 - min_from_1 - 2)
        print("=========== cheat (end2)", cheat)
    else:
        if not around1 or not around2:
            return 0
        cheat = max(max(around2) - min(around1), max(around1) - min(around2)) - 3
        print("=========== cheat (all!)", cheat)

    if cheat < 0:
        return 0
    return cheat


xmap = SafeMap(lines)
xmap.show()
end_coords = xmap.find(END)

paint_walk(xmap)

# this is to understand numbering
width = len(xmap.xmap[0])
print("---" * width)
for row in xmap.xmap:
    print("".join(f"{item:3d}" if isinstance(item, int) else item * 3 for item in row))
print("---" * width)

all_reduced = {}

# horizontal pairs
for y, row in enumerate(xmap.xmap[1:-1], 1):  # avoid external walls
    for x, item in enumerate(row[1:-2], 1):  # avoid external walls and last as we do +1
        tile1 = (x, y)
        tile2 = (x + 1, y)
        cheat = search(xmap, tile1, tile2, end_coords)
        all_reduced.setdefault(cheat, []).append((tile1, tile2))

# vertical pairs
for y, row in enumerate(xmap.xmap[1:-2], 1):  # avoid external walls and last as we do +1
    for x, item in enumerate(row[1:-1], 1):  # avoid external walls
        tile1 = (x, y)
        tile2 = (x, y + 1)
        cheat = search(xmap, tile1, tile2, end_coords)
        all_reduced.setdefault(cheat, []).append((tile1, tile2))

del all_reduced[0]
cnt_reduced = Counter({cheat: len(tiles) for cheat, tiles in all_reduced.items()})
for cheat, quant in cnt_reduced.most_common():
    print(cheat, quant, all_reduced[cheat])

total = cnt_reduced
print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")

breakpoint()
print(">=100ps:", sum([quant for cheat, quant in cnt_reduced.items() if cheat >= 100]))
