import sys
from collections import defaultdict
from itertools import combinations

lines = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()

xmap = [list(line) for line in lines]
max_x = len(xmap[0])
max_y = len(xmap)

antennas = defaultdict(list)
for y, row in enumerate(xmap):
    for x, char in enumerate(row):
        if char != ".":
            antennas[char].append((x, y))

antinodes = set()
for antenna, positions in antennas.items():
    print("======= antenna", repr(antenna), positions)
    for (x1, y1), (x2, y2) in combinations(positions, 2):
        print("======= coords", (x1, y1), (x2, y2))
        dx = x2 - x1
        dy = y2 - y1

        an1_x = x1 - dx
        an1_y = y1 - dy
        print("======= an1", (an1_x, an1_y))
        if (0 <= an1_x < max_x) and (0 <= an1_y < max_y):
            print("============= ok!")
            antinodes.add((an1_x, an1_y))

        an2_x = x2 + dx
        an2_y = y2 + dy
        print("======= an2", (an1_x, an1_y))
        if (0 <= an2_x < max_x) and (0 <= an2_y < max_y):
            print("============= ok!")
            antinodes.add((an2_x, an2_y))


total = len(antinodes)
print("Total:", total)
