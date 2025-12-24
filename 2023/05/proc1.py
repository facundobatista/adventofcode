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
                print("====== map!", repr(title), thismap)
                return allmaps
            if not nline:
                break
            dest_start, source_start, length = map(int, nline.split())
            source_range = range(source_start, source_start + length)
            thismap.append((source_range, dest_start - source_start))
        print("====== map!", repr(title), thismap)


# load everything
lines = iter(lines)

# special, seeds
line = next(lines)
title, values = line.split(":")
assert title == "seeds"
seeds = [int(x.strip()) for x in values.split()]
line = next(lines)
assert not line.strip()

# maps
allmaps = _loadmaps(lines)
print(f"Loaded! seeds={len(seeds)} maps={allmaps.keys()}")

steps = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]
data = dict(seed=seeds)
lowest = 9999999999999999999999999999999999999999999999999999999
for seedrange in seeds:
    print("===== seeds", seedrange)
    for seed in seedrange:
        datum = seed
        for datasrc, datanext in sliding_window(steps, 2):
            # print("======== pair", datasrc, datanext)
            themap = allmaps[(datasrc, datanext)]
            for srcrange, delta in themap:
                if datum in srcrange:
                    datum += delta
                    break
            # print("======== got", datum)
        # print("====== final!", datum)
        lowest = min(datum, lowest)
print("Lowest", lowest)
