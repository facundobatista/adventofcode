import itertools
import sys

lines = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()


# build the map
themap = [list(line) for line in lines]


def _expand(themap):
    to_insert = []
    width = len(themap[0])
    for idx, row in enumerate(themap):
        print("====== R", row)
        if set(row) == {"."}:
            to_insert.append(idx)
    print("==== expand", to_insert)
    for idx in reversed(to_insert):
        themap.insert(idx, ["."] * width)
    return themap


# expand it vertical
themap = _expand(themap)

# expand it horizontal
translated = list(zip(*themap))
expanded = _expand(translated)
themap = list(zip(*expanded))

print("===== expanded")
for x in themap:
    print(x)

# locate galaxy positions
galaxies = []
for pos_y, row in enumerate(themap):
    for pos_x, item in enumerate(row):
        if item == "#":
            galaxies.append((pos_x, pos_y))

print("==== galaxies", galaxies)


def _distance(g1, g2):
    return abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])


total = 0
for g1, g2 in itertools.combinations(galaxies, 2):
    total += _distance(g1, g2)
print("====== total", total)
