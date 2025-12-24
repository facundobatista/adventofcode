import sys

lines = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""
should_result = 45

# lines = """
# #################
# #...#...#...#..E#
# #.#.#.#.#.#.#.#.#
# #.#.#.#...#...#.#
# #.#.#.#.###.#.#.#
# #...#.#.#.....#.#
# #.#.#.#.#.#####.#
# #.#...#.#.#.....#
# #.#.#####.#.###.#
# #.#.#.......#...#
# #.#.###.#####.###
# #.#.#...#.....#.#
# #.#.#.#####.###.#
# #.#.#.........#.#
# #.#.#.#########.#
# #S#.............#
# #################
# """
# should_result = 64
#
# lines = """
# #####
# ###E#
# ###.#
# #S..#
# #####
# """
# should_result = 5

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
    should_result = 105496
else:
    print("Bad arg")
    exit()


class SafeMap:

    # deltas
    DELTA_RIGHT = (1, 0)
    DELTA_LEFT = (-1, 0)
    DELTA_UP = (0, -1)
    DELTA_DOWN = (0, 1)

    def __init__(self, lines):
        self.xmap = [list(line) for line in lines]
        self.max_x = len(self.xmap[0])
        self.max_y = len(self.xmap)

    def __getitem__(self, coord):
        x, y = coord
        if (0 <= x < self.max_x) and (0 <= y < self.max_y):
            val = self.xmap[y][x]
        else:
            raise ValueError("out of map")
        return val

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
        for row in self.xmap:
            print("".join(item for item in row))
        print("-" * len(row))

    def find(self, to_find):
        """Return the first ocurrence of item."""
        for y, row in enumerate(self.xmap):
            for x, item in enumerate(row):
                if item == to_find:
                    return x, y
        raise ValueError("Couldn't find " + repr(to_find))


xmap = SafeMap(lines)

# map constants
START = "S"
END = "E"
WALL = "#"

# direction constants
DIR_RIGHT, DIR_LEFT, DIR_UP, DIR_DOWN = "dir-right", "dir-left", "dir-up", "dir-down"

# delta of possible next position, and info for the movement
EXPLORATION = [
    (xmap.DELTA_RIGHT, DIR_RIGHT),
    (xmap.DELTA_LEFT, DIR_LEFT),
    (xmap.DELTA_UP, DIR_UP),
    (xmap.DELTA_DOWN, DIR_DOWN),
]
COST = {
    (DIR_RIGHT, xmap.DELTA_RIGHT): 1,
    (DIR_RIGHT, xmap.DELTA_LEFT): None,
    (DIR_RIGHT, xmap.DELTA_UP): 1001,
    (DIR_RIGHT, xmap.DELTA_DOWN): 1001,
    (DIR_LEFT, xmap.DELTA_RIGHT): None,
    (DIR_LEFT, xmap.DELTA_LEFT): 1,
    (DIR_LEFT, xmap.DELTA_UP): 1001,
    (DIR_LEFT, xmap.DELTA_DOWN): 1001,
    (DIR_UP, xmap.DELTA_RIGHT): 1001,
    (DIR_UP, xmap.DELTA_LEFT): 1001,
    (DIR_UP, xmap.DELTA_UP): 1,
    (DIR_UP, xmap.DELTA_DOWN): None,
    (DIR_DOWN, xmap.DELTA_RIGHT): 1001,
    (DIR_DOWN, xmap.DELTA_LEFT): 1001,
    (DIR_DOWN, xmap.DELTA_UP): None,
    (DIR_DOWN, xmap.DELTA_DOWN): 1,
}


class Node:
    def __init__(self, x, y, direc, parent):
        self.x = x
        self.y = y
        self.direc = direc
        self.parent = parent

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.direc == other.direc

    def __hash__(self):
        return hash((self.x, self.y, self.direc))


def walk():
    prev_walks = {}
    paths_score = []

    start_x, start_y = xmap.find(START)
    stack = [(0, Node(start_x, start_y, None, None))]

    while stack:
        # cur_x and cur_y: current coord
        # cur_dir: the current direction, how it arrived to current coord
        # path_score: the score so far, to avoid going further if this is already too long
        path_score, cur_node = stack.pop()
        # print("====== walk!", (cur_x, cur_y, cur_dir, path_score))

        # if we get to the tile, coming from the same direction, and with higher
        # path score no point in continuing that path because previous exploration
        # is better -- this also prevents loops
        key = (cur_node.x, cur_node.y, cur_node.direc)
        prev_score = prev_walks.get(key)
        if prev_score is not None and prev_score < path_score:
            continue
        prev_walks[key] = path_score

        for (dx, dy), new_dir in EXPLORATION:
            new_x = cur_node.x + dx
            new_y = cur_node.y + dy
            new_tile = xmap[(new_x, new_y)]
            if cur_node.direc is None:
                # we're *starting* in this direction, cost is 1
                move_cost = 1
            else:
                move_cost = COST[(cur_node.direc, (dx, dy))]
            # print(sep, "======== explor", (new_x, new_y, new_tile, move_cost))
            if move_cost is None:
                # trying to go back to last square,
                continue

            if new_tile == WALL:
                # a wall! can't go
                continue

            new_path_score = path_score + move_cost

            if new_tile == END:
                # this is the end, beautiful friend, this is the end, my only friend, the end
                print("=========== END!", new_path_score)
                path_nodes_tiles = {(new_x, new_y)}  # preloaded with END
                backtrace_node = cur_node
                while backtrace_node is not None:
                    path_nodes_tiles.add((backtrace_node.x, backtrace_node.y))
                    backtrace_node = backtrace_node.parent
                paths_score.append((new_path_score, path_nodes_tiles))
                continue

            stack.append((new_path_score, Node(new_x, new_y, new_dir, cur_node)))

    print("==== paths_score")
    for x in paths_score:
        print("======== x", x[0], len(x[1]))
    min_score = min(score for score, path in paths_score)
    print("======== min!", min_score)
    all_tiles = set()
    for score, path in paths_score:
        if score == min_score:
            all_tiles.update(path)

    return len(all_tiles)


total = walk()


print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
