import itertools
import sys

lines = """
AAAA
BBCD
BBCC
EEEC
"""
should_result = 80

lines = """
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""
should_result = 436

lines = """
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
"""
should_result = 236

lines = """
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""
should_result = 368

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
should_result = 1206


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


class RealMap:
    def __init__(self, prefill=False):
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

    def mark(self, coord, value=None):
        x, y = coord
        self.xmap[y][x] = value


class RegionMap:
    def __init__(self, region):
        self.max_x = len(lines[0])
        self.max_y = len(lines)
        self.xmap = [[0] * self.max_x for _ in range(self.max_y)]

        for x, y in region:
            self.xmap[y][x] = 1

    def __getitem__(self, coord):
        x, y = coord
        if (0 <= x < self.max_x) and (0 <= y < self.max_y):
            val = self.xmap[y][x]
        else:
            val = 0
        return val


xmap = RealMap()


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
    # print("Walking")
    for x, y in itertools.product(range(xmap.max_x), range(xmap.max_y)):
        plant = xmap[(x, y)]
        if plant is not None:
            break
    else:
        return

    # print("    found new region", x, y, plant)
    region = []
    develop(plant, region, x, y)
    return region


regions = []
while True:
    region = find_new_region()
    # print("    developed", region)
    if region is None:
        break
    regions.append(region)


# def get_sides(region):
#     """Walk through the "edges" to find sides.
#
#     Start from initial coord in the region, because how is found it guarantees that it has
#     a "roof side". Walk clockwise.
#     """
#     # for each direction, how to check if the edge continues; first value is the cell to check
#     exploratory = [
#         "right": ((1, 0), (1, -1)),
#
#

def get_sides(region):
    """Traverse map horizontally and vertically.

    On each direction, do one step at the time. For each cell, record transitions, then
    find consecutive ones.

    To find a transition we cannot use the plant type, as different regions may have the same
    plant. So we get a map and "turn off" all that is not a region. We set them to , and
    1 the ones in the region, so when traversing we don't need to do a comparison.

    We subtract the difference from cells, so transitions are 1 or -1 (which correspond to
    different sides!)
    """
    xmap = RegionMap(region)
    total_sides = 0
    print("======== processing region", region)

    # traverse with a column moving horizontally
    for x in range(xmap.max_x + 1):  # extra one because they are edges!
        transitions = []
        for y in range(xmap.max_y):
            transitions.append(xmap[(x - 1, y)] - xmap[(x, y)])
        # print("======= horiz", x, transitions)
        deduplicated = [key for key, _ in itertools.groupby(transitions)]
        sides = sum(x != 0 for x in deduplicated)
        # print("======= dedupl.", deduplicated, sides)
        total_sides += sides

    # traverse with a row moving vertically
    for y in range(xmap.max_y + 1):  # extra one because they are edges!
        transitions = []
        for x in range(xmap.max_x):
            transitions.append(xmap[(x, y - 1)] - xmap[(x, y)])
        # print("======= vert.", x, transitions)
        deduplicated = [key for key, _ in itertools.groupby(transitions)]
        sides = sum(x != 0 for x in deduplicated)
        # print("======= deduplic", deduplicated, sides)
        total_sides += sides

    return total_sides


cost = 0
for region in regions:
    sides = get_sides(region)
    area = len(region)
    print("===========      s a", sides, area)
    cost += sides * area


print("Total:", cost)
if should_result is not None:
    print("ok :)" if should_result == cost else f"MAL! debería: {should_result!r}")
