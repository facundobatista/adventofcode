import itertools
import sys

lines = """
AAAA
BBCD
BBCC
EEEC
"""
should_result = 140

lines = """
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""
should_result = 772

lines = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""
should_result = 1930

if len(sys.argv) != 2:
    print("test or real?")
    exit()
if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
    should_result = None
else:
    print("Bad arg")
    exit()


class Map:
    def __init__(self):
        self.xmap = [list(line) for line in lines]
        self.max_x = len(self.xmap[0])
        self.max_y = len(self.xmap)

    def __getitem__(self, coord):
        x, y = coord
        if (0 <= x < self.max_x) and (0 <= y < self.max_y):
            val = self.xmap[y][x]
        else:
            val = None
        return val

    def mark(self, coord):
        x, y = coord
        self.xmap[y][x] = None


xmap = Map()


def develop(plant, region, x, y):
    # add starting coords to the region
    region.append((x, y))
    xmap.mark((x, y))

    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        ncoord = (x + dx, y + dy)
        new_plant = xmap[ncoord]
        if new_plant == plant:
            develop(plant, region, *ncoord)


def find_new_region():
    print("Walking")
    for x, y in itertools.product(range(xmap.max_x), range(xmap.max_y)):
        plant = xmap[(x, y)]
        if plant is not None:
            break
    else:
        return

    print("    found new region", x, y, plant)
    region = []
    develop(plant, region, x, y)
    return region


regions = []
while True:
    region = find_new_region()
    print("    developed", region)
    if region is None:
        break
    regions.append(region)


def get_perimeter(region):
    borders = 0
    region = set(region)
    for x, y in region:
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ncoord = (x + dx, y + dy)
            if ncoord not in region:
                borders += 1
    return borders


cost = 0
for region in regions:
    print("======== processing region", region)
    perimeter = get_perimeter(region)
    area = len(region)
    print("===========      p a", perimeter, area)
    cost += perimeter * area


print("Total:", cost)
if should_result is not None:
    print("ok :)" if should_result == cost else f"MAL! debería: {should_result!r}")
