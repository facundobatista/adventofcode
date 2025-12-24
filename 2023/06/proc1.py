import sys

lines = """
Time:      7  15   30
Distance:  9  40  200
"""

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()


def _get_ww(time, distance):
    print("====== T, D", time, distance)
    wways = 0
    for pressing in range(1, time):
        traveling = time - pressing
        farout = traveling * pressing
        if farout > distance:
            wways += 1
    print("====   ways", wways)
    return wways


# load everything
line1, line2 = lines
title, values = line1.split(":")
assert title == "Time"
times = [int(x.strip()) for x in values.split()]
title, values = line2.split(":")
assert title == "Distance"
distances = [int(x.strip()) for x in values.split()]

winningways = 1
for time, distance in zip(times, distances):
    winningways *= _get_ww(time, distance)

print("Total", winningways)
