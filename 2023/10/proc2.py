import sys

lines = """
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""
lines = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
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
        self.themap = [list(line) for line in lines]
        self.width = len(self.themap[0])
        self.height = len(self.themap)

    def __getitem__(self, xy):
        x, y = xy
        if x < 0 or x >= self.width:
            return None
        if y < 0 or y >= self.height:
            return None
        element = self.themap[y][x]
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
start_connections = []
first_conn = None
for dx, dy in around:
    pos_x = start_x + dx
    pos_y = start_y + dy
    element = area[pos_x, pos_y]
    coming_from_x = -dx
    coming_from_y = -dy
    if (element, coming_from_x, coming_from_y) in possibilities:
        print("====== found", element, coming_from_x, coming_from_y)
        if first_conn is None:
            first_conn = (pos_x, pos_y, element, coming_from_x, coming_from_y)
        start_connections.append((dx, dy))

print("==== start conn", start_connections)
# walk the tube, record the path
pos_x, pos_y, element, coming_from_x, coming_from_y = first_conn
tube_parts = [(start_x, start_y), (pos_x, pos_y)]
while True:
    dx, dy = possibilities[element, coming_from_x, coming_from_y]

    # move
    next_x = pos_x + dx
    next_y = pos_y + dy
    element = area[next_x, next_y]
    if element == "S":
        break
    coming_from_x, coming_from_y = -dx, -dy
    pos_x, pos_y = next_x, next_y
    tube_parts.append((pos_x, pos_y))

print("========= tube parts", tube_parts)

# replace S by a proper tube so we know how it "encloses" other slots
start_connections = set(start_connections)
if start_connections == {(0, 1), (1, 0)}:
    s_replace = "F"
elif start_connections == {(0, -1), (1, 0)}:
    s_replace = "L"
elif start_connections == {(0, 1), (-1, 0)}:
    s_replace = "7"
elif start_connections == {(0, -1), (-1, 0)}:
    s_replace = "J"
area.themap[start_y][start_x] = s_replace

# scan the map horizontally, from left to right, flagging what's between tube walls
found_inside = []
for idx_y, row in enumerate(area.themap):

    inside = False
    tubeswall = []
    for idx_x, pipe in enumerate(row):
        print("========= scan", (idx_x, idx_y), pipe, inside)
        if (idx_x, idx_y) in tube_parts:
            print("============= tube part!", pipe)
            tubeswall.append(pipe)
        else:
            if tubeswall:
                # finished crossing some tubes
                print("====== finished, tubes", tubeswall)
                wall = "".join(tubeswall)
                wall = wall.replace("-", "")
                wall = wall.replace("F7", "")
                wall = wall.replace("LJ", "")
                wall = wall.replace("L7", "|")
                wall = wall.replace("FJ", "|")
                print("====== finished, wall!", repr(wall))
                if len(wall) % 2:
                    inside = not inside
                print(f"======== leaving inside={inside}")
                tubeswall = []

            # whatever else
            print("============= else", pipe)
            if inside:
                print("================= XXX")
                found_inside.append((idx_x, idx_y))

print("Found inside", len(found_inside), found_inside)
