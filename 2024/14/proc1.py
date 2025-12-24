import re
import sys

lines = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""
tiles_wide = 11
tiles_tall = 7
should_result = 12


if len(sys.argv) != 2:
    print("test or real?")
    exit()
if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
    tiles_wide = 101
    tiles_tall = 103
    should_result = None
else:
    print("Bad arg")
    exit()


# class RegionMap:
#     def __init__(self, region):
#         self.max_x = len(lines[0])
#         self.max_y = len(lines)
#         self.xmap = [[0] * self.max_x for _ in range(self.max_y)]
#
#         for x, y in region:
#             self.xmap[y][x] = 1
#
#     def __getitem__(self, coord):
#         x, y = coord
#         if (0 <= x < self.max_x) and (0 <= y < self.max_y):
#             val = self.xmap[y][x]
#         else:
#             val = 0
#         return val
#
#
# xmap = RealMap()


# load robots and velocities


posits = []
veloxs = []
for line in lines:
    px, py, vx, vy = re.match(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", line.strip()).groups()
    posits.append((int(px), int(py)))
    veloxs.append((int(vx), int(vy)))
print("====== posits", posits)
print("====== veloxs", veloxs)

nsteps = 100
final_posits = []
for (px, py), (vx, vy) in zip(posits, veloxs):
    npx = px + vx * nsteps
    npy = py + vy * nsteps

    # they wrap
    npx = npx % tiles_wide
    npy = npy % tiles_tall
    final_posits.append((npx, npy))
print("====== new ps", final_posits)

# remove the ones in the middle cross
mid_wide = tiles_wide // 2
mid_tall = tiles_tall // 2
cleaned = [(x, y) for x, y in final_posits if x != mid_wide and y != mid_tall]

#  1 2
#  3 4
r_q1 = len([1 for x, y in cleaned if x < mid_wide and y < mid_tall])
r_q2 = len([1 for x, y in cleaned if x > mid_wide and y < mid_tall])
r_q3 = len([1 for x, y in cleaned if x < mid_wide and y > mid_tall])
r_q4 = len([1 for x, y in cleaned if x > mid_wide and y > mid_tall])
print("======== quadrants", r_q1, r_q2, r_q3, r_q4)
total = r_q1 * r_q2 * r_q3 * r_q4

print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
