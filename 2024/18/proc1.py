import sys

lines = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""
rain_length = 12
mem_space = (7, 7)
should_result = 22


if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
    rain_length = 1024
    mem_space = (71, 71)
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
CORRUPTED = "#"

# direction constants
DIR_RIGHT, DIR_LEFT, DIR_UP, DIR_DOWN = "dir-right", "dir-left", "dir-up", "dir-down"

# delta of possible next position, and info for the movement
EXPLORATION = [
    SafeMap.DELTA_LEFT,
    SafeMap.DELTA_DOWN,
    SafeMap.DELTA_RIGHT,
    SafeMap.DELTA_UP,
]


def walk():
    min_score = sys.maxsize

    start_x, start_y = 0, 0
    end_x, end_y = (mem_space[0] - 1, mem_space[1] - 1)
    stack = [(start_x, start_y, 0)]

    # keep here the lowest path length to get to a tile; if walked in previously with shorter
    # path than current, no point in going there
    walked = {}

    while stack:
        # cur_x and cur_y: current coord
        # cur_dir: the current direction, how it arrived to current coord
        # path_score: the score so far, to avoid going further if this is already too long
        cur_x, cur_y, cur_len = stack.pop()
        # sep = "  " * len(path)
        # print(sep, "====== walk!", (cur_x, cur_y, path))

        for dx, dy in EXPLORATION:
            new_x = cur_x + dx
            new_y = cur_y + dy
            new_len = cur_len + 1

            if new_x == end_x and new_y == end_y:
                # this is the end, beautiful friend, this is the end, my only friend, the end
                print("=========== END!", new_len)
                min_score = min(new_len, min_score)
                continue

            new_coords = (new_x, new_y)
            new_tile = xmap[new_coords]
            # print(sep, "======== explor", (new_x, new_y, new_tile))

            if new_tile == CORRUPTED:
                # a wall! can't go
                continue

            prev_len = walked.get(new_coords)
            if prev_len is not None and prev_len <= new_len:
                # been there before with a shorter path
                continue
            walked[new_coords] = new_len

            stack.append((new_x, new_y, new_len))

    return min_score


w, h = mem_space
xmap = SafeMap([[TILE_OK] * w for _ in range(h)], out_of_map=CORRUPTED)
rain_bytes = [map(int, line.split(",")) for line in lines]
for rain_x, rain_y in rain_bytes[:rain_length]:
    xmap[(rain_x, rain_y)] = CORRUPTED
print(xmap.show())

total = walk()


print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
