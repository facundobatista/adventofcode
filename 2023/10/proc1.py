import sys

# lines = """
# .....
# .S-7.
# .|.|.
# .L-J.
# .....
# """
lines = """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""

#   | is a vertical pipe connecting north and south.
#   - is a horizontal pipe connecting east and west.
#   L is a 90-degree bend connecting north and east.
#   J is a 90-degree bend connecting north and west.
#   7 is a 90-degree bend connecting south and west.
#   F is a 90-degree bend connecting south and east.
#   . is ground; there is no pipe in this tile.
#   S is the starting position of the animal


if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()


class Area:
    def __init__(self):
        self.themap = list(lines)
        self.width = len(self.themap[0])
        self.height = len(self.themap)

    def __getitem__(self, xy):
        print("======= XY", repr(xy))
        x, y = xy
        if x < 0 or x >= self.width:
            return None
        if y < 0 or y >= self.height:
            return None
        element = self.themap[y][x]
        print("=======  e", element)
        return element


# search S
area = Area()
for start_y, row in enumerate(area.themap):
    if "S" in row:
        start_x = row.index("S")
        break
print("===== start!", start_x, start_y)

# find any connection to S
rawposs = [
    ("|", (0, -1), (0, 1)),
    ("L", (0, -1), (1, 0)),
    ("J", (0, -1), (-1, 0)),
    ("7", (0, 1), (-1, 0)),
    ("F", (0, 1), (1, 0)),
    ("-", (1, 0), (-1, 0)),
]

possibilities = {}  # pipe, input dx and dy =>, output dx and dy
for pipe, o1, o2 in rawposs:
    possibilities[(pipe, *o1)] = o2
    possibilities[(pipe, *o2)] = o1

# find first connection
around = [(0, 1), (0, -1), (-1, 0), (1, 0)]
for dx, dy in around:
    pos_x = start_x + dx
    pos_y = start_y + dy
    element = area[pos_x, pos_y]
    coming_from_x = -dx
    coming_from_y = -dy
    if (element, coming_from_x, coming_from_y) in possibilities:
        print("====== found", element, coming_from_x, coming_from_y)
        break

# walk the tube
steps = 1  # because we already started walking
while True:
    dx, dy = possibilities[element, coming_from_x, coming_from_y]

    # move
    steps += 1
    next_x = pos_x + dx
    next_y = pos_y + dy
    element = area[next_x, next_y]
    print("=========== EEE", element)
    if element == "S":
        break
    coming_from_x, coming_from_y = -dx, -dy
    pos_x, pos_y = next_x, next_y

print("Far away:", steps / 2)
