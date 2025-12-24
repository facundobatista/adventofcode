import sys

lines = """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""
should_result = 2028

lines = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""
should_result = 10092


if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
    should_result = None
else:
    print("Bad arg")
    exit()


class SafeMap:
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
        for row in self.xmap:
            print("".join(item for item in row))
        print("-" * len(row))


store = map_lines = []
mov_lines = []
for line in lines:
    line = line.strip()
    if line:
        store.append(line)
    else:
        store = mov_lines

xmap = SafeMap(map_lines)
movements = "".join(mov_lines)

mov_to_delta = {
    "<": (-1, 0),
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
}
ROBOT = "@"
BOX = "O"
WALL = "#"

for y, line in enumerate(lines):
    for x, char in enumerate(line):
        if char == ROBOT:
            rob_x, rob_y = x, y


def find_next_empty(rob_x, rob_y, dx, dy):
    """Finds next empty element between robot and a wall.

    Return the list of boxes and the robot to move 1 to fill that position, or None if none found.
    """
    cur_x = rob_x
    cur_y = rob_y
    to_later_move = [(rob_x, rob_y)]  # start with the robot, because it will move if it can
    while True:
        nx = cur_x + dx
        ny = cur_y + dy
        nchar = xmap[(nx, ny)]
        if nchar == WALL:
            # found a wall without finding an empty position before, can't move
            return
        if nchar == ".":
            # empty! fill this one
            return to_later_move

        # box!
        assert nchar == BOX, repr(nchar)
        to_later_move.append((nx, ny))
        cur_x = nx
        cur_y = ny


for mov in movements:
    print("========== move?", repr(mov), rob_x, rob_y)
    dx, dy = mov_to_delta[mov]
    to_move = find_next_empty(rob_x, rob_y, dx, dy)
    print("==========  ??", to_move)
    if to_move is None:
        continue

    # move sequence "elegantely" (one by one)
    for coord in reversed(to_move):
        moved_x, moved_y = xmap.switch(coord, (dx, dy))
    xmap.show()
    rob_x, rob_y = moved_x, moved_y  # as it's the last to be moved


# sum boxes positions
total = 0
for x in range(xmap.max_x):
    for y in range(xmap.max_y):
        item = xmap[(x, y)]
        if item == BOX:
            total += x + 100 * y

print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
