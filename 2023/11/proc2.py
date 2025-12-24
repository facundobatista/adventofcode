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
x_expand_points = []
y_expand_points = []


def _calculate_expand(themap, expand_points):
    for idx, row in enumerate(themap):
        if set(row) == {"."}:
            expand_points.append(idx)


# expand it vertical
_calculate_expand(themap, y_expand_points)

# expand it horizontal
translated = list(zip(*themap))
_calculate_expand(translated, x_expand_points)

print("===== x exp points", x_expand_points)
print("===== y exp points", y_expand_points)

# locate galaxy positions in unexpanded universe
galaxies = []
for pos_y, row in enumerate(themap):
    for pos_x, item in enumerate(row):
        if item == "#":
            galaxies.append((pos_x, pos_y))

print("==== galaxies raw", galaxies)

# "expand" positions
expansion_factor = 999999
for expand_point in reversed(x_expand_points):
    for idx, (gx, gy) in enumerate(galaxies):
        if gx > expand_point:
            galaxies[idx] = (gx + expansion_factor, gy)
for expand_point in reversed(y_expand_points):
    for idx, (gx, gy) in enumerate(galaxies):
        if gy > expand_point:
            galaxies[idx] = (gx, gy + expansion_factor)

print("==== galaxies xpd", galaxies)


def _distance(g1, g2):
    return abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])


total = 0
for g1, g2 in itertools.combinations(galaxies, 2):
    total += _distance(g1, g2)
print("====== total", total)
