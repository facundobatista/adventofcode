import collections
import itertools
import sys

lines = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
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


def extrapolate(sequence):
    print("======= extrap", sequence)

    # reduce, keeping last numbers if not done
    lastnums = [sequence[-1]]
    while True:
        sequence = [b - a for a, b in sliding_window(sequence, 2)]
        print("========= reduc", sequence)
        if set(sequence) == {0}:
            break
        lastnums.append(sequence[-1])

    # the extrapolated value is the sum of all last digits
    print("===== last nums", lastnums)
    extrapolated = sum(lastnums)
    print("===== extrap", extrapolated)
    return extrapolated


total = 0
for line in lines:
    extra_value = extrapolate(list(map(int, line.split())))
    total += extra_value
print("Total:", total)
