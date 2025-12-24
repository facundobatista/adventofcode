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
    antinodes.update((x, y) for x, y in positions)

    for (x1, y1), (x2, y2) in combinations(positions, 2):
        print("======= coords", (x1, y1), (x2, y2))
        dx = x2 - x1
        dy = y2 - y1

        base_x = x1
        base_y = y1
        while True:
            an_x = base_x - dx
            an_y = base_y - dy
            print("======= an1", (an_x, an_y))
            if (0 <= an_x < max_x) and (0 <= an_y < max_y):
                print("============= ok!")
                antinodes.add((an_x, an_y))
                base_x = an_x
                base_y = an_y
            else:
                print("============= out")
                break

        base_x = x2
        base_y = y2
        while True:
            an_x = base_x + dx
            an_y = base_y + dy
            print("======= an2", (an_x, an_y))
            if (0 <= an_x < max_x) and (0 <= an_y < max_y):
                print("============= ok!")
                antinodes.add((an_x, an_y))
                base_x = an_x
                base_y = an_y
            else:
                print("============= out")
                break

total = len(antinodes)
print("Total:", total)
