import collections
import itertools
import sys

lines = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()


def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(itertools.islice(it, n - 1), maxlen=n)
    for x in it:
        window.append(x)
        yield tuple(window)


def _loadmaps(lines):
    allmaps = {}
    while True:
        title, flag = next(lines).strip().split()
        thismap = allmaps[tuple(title.split("-to-"))] = []
        assert flag == "map:"
        while True:
            try:
                nline = next(lines).strip()
            except StopIteration:
                return allmaps
            if not nline:
                break
            dest_start, source_start, length = map(int, nline.split())
            source_range = range(source_start, source_start + length)
            thismap.append((source_range, dest_start - source_start))


# load everything
lines = iter(lines)

# special, seeds
line = next(lines)
title, values = line.split(":")
assert title == "seeds"
seeds = []
svals = iter(values.split())
while True:
    try:
        v1 = int(next(svals))
        v2 = int(next(svals))
    except StopIteration:
        break
    # print("======== V", v1, v2)
    seeds.append(range(v1, v1 + v2))
line = next(lines)
assert not line.strip()

# maps
allmaps = _loadmaps(lines)
for title, themap in allmaps.items():
    themap.sort(key=lambda r_d: r_d[0].start)
    print("====== map!", repr(title), themap)

    # ensure no holes
    newmap = []
    for (r1, d1), (r2, d2) in sliding_window(themap, 2):
        print("==== r1, r2", r1, r2)
        newmap.append((r1, d1))
        if r1.stop > r2.start:
            raise ValueError("Maps overlays")
        if r1.stop < r2.start:
            print("========== FILLING")
            newmap.append((range(r1.stop, r2.start), 0))
    newmap.append((r2, d2))
    themap[:] = newmap
    print("====== map!", repr(title), themap)


print(f"Loaded! seeds={len(seeds)} maps={allmaps.keys()}")

steps = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]


# def _overlap(inprange, srcrange, delta):
#     print("===== overlap", inprange, srcrange, delta)
#     result = []
#
#     if inprange.stop <= srcrange.start:
#         # input is complete below
#         result.append(inprange)
#
#     elif inprange.start >= srcrange.stop:
#         # input is complete above
#         result.append(inprange)
#
#     elif inprange.start >= srcrange.start and inprange.stop <= srcrange.stop:
#         # completely inside
#         result.append(range(inprange.start + delta, inprange.stop + delta))
#
#     elif inprange.start < srcrange.start and inprange.stop <= srcrange.stop:
#         # partially below, partially inside
#         result.append(range(inprange.start, srcrange.start))
#         result.append(range(srcrange.start + delta, inprange.stop + delta))
#
#     elif inprange.start >= srcrange.start and inprange.stop > srcrange.stop:
#         # partially inside, partially above
#         result.append(range(inprange.start + delta, srcrange.stop + delta))
#         result.append(range(srcrange.stop, inprange.stop))
#
#     elif inprange.start < srcrange.start and inprange.stop > srcrange.stop:
#         # starts below, ends above (wraps it)
#         result.append(range(inprange.start, srcrange.start))
#         result.append(range(srcrange.start + delta, srcrange.stop + delta))
#         result.append(range(srcrange.stop, inprange.stop))
#
#     else:
#         raise ValueError("WTF")
#
#     print("=====     GOT", result)
#     return result


def _overlap(inprange, themap):
    print("===== overlap", inprange, themap)
    result = []

    movingstart = inprange.start
    firstsrc = themap[0][0]
    if movingstart < firstsrc.start:
        # before the sequence
        print("=====     starts before")
        if inprange.stop < firstsrc.start:
            # COMPLETELY before the sequence
            print("=====     completely before")
            return [inprange]

        result.append(range(movingstart, firstsrc.start))
        movingstart = firstsrc.start

    for srcrange, delta in themap:
        print("=========== ev", srcrange)
        if movingstart >= srcrange.stop:
            # not there yet
            print("          skip")
            continue

        if inprange.stop <= srcrange.stop:
            # finishes in this one
            result.append(range(movingstart + delta, inprange.stop + delta))
            print("          end")
            break

        # input is in current source
        print("          here")
        result.append(range(movingstart + delta, srcrange.stop + delta))
        movingstart = srcrange.stop

    else:
        # finishes after latest item in the map
        result.append(range(movingstart, inprange.stop))

    print("=====     GOT", result)
    return result


inputranges = seeds
for datasrc, datanext in sliding_window(steps, 2):
    print("======== map", datasrc, datanext)
    themap = allmaps[(datasrc, datanext)]

    newranges = set()
    for inprange in inputranges:
        newranges.update(_overlap(inprange, themap))
    print("======== new ranges", newranges)
    inputranges = newranges
print("====== final!", inputranges)

lowest = 9999999999999999999999999999999999999999999999999999999
for finalrange in inputranges:
    lowest = min(finalrange.start, lowest)
print("Lowest", lowest)
