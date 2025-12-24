import re
import sys
import time

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


if len(sys.argv) != 2:
    print("test or real?")
    exit()
if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
    tiles_wide = 101
    tiles_tall = 103
else:
    print("Bad arg")
    exit()


# load robots and velocities
posits = []
veloxs = []
for line in lines:
    px, py, vx, vy = re.match(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", line.strip()).groups()
    posits.append((int(px), int(py)))
    veloxs.append((int(vx), int(vy)))


def show(posits):
    posits_set = set(posits)
    for y in range(tiles_tall):
        row = []
        for x in range(tiles_wide):
            row.append("X" if (x, y) in posits_set else " ")
        print("".join(row))
    print("-" * tiles_wide)


r_x_from = tiles_wide / 3
r_x_to = 2 * tiles_wide / 3
r_y_from = tiles_tall / 3
r_y_to = 2 * tiles_tall / 3

print("-" * tiles_wide)
for step in range(1, 10010):
    new_posits = []
    for (px, py), (vx, vy) in zip(posits, veloxs):
        npx = px + vx
        npy = py + vy

        # they wrap
        npx = npx % tiles_wide
        npy = npy % tiles_tall
        new_posits.append((npx, npy))
    posits = new_posits

    q_center = len([1 for (x, y) in posits if (r_x_from < x < r_x_to) and (r_y_from < y < r_y_to)])
    q_outside = len(posits) - q_center
    if q_center > q_outside:
        print("===== step", step, q_center, q_outside)
        show(posits)
        time.sleep(.2)
        break
