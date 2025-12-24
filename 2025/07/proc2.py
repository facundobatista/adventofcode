test_lines = """
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
"""
expected_test_result = 40

SOURCE = "S"
SPLITTER = "^"

_cache = {}


def explore(splitters, idx, beam):
    # print("============= explore", idx, beam)
    if idx == len(splitters):
        # print("======== bottom")
        return 1

    key = (idx, beam)
    if key in _cache:
        return _cache[key]

    sublines = 0
    if beam in splitters[idx]:
        sublines += explore(splitters, idx + 1, beam - 1)
        sublines += explore(splitters, idx + 1, beam + 1)
    else:
        sublines += explore(splitters, idx + 1, beam)

    _cache[key] = sublines
    return sublines


def run(lines):
    beam = lines[0].index(SOURCE)

    # prefilter the lines and only get the splitter positions (if any)
    splitters = []
    for line in lines[1:]:
        in_this_line = {idx for idx, item in enumerate(line) if item == SPLITTER}
        if in_this_line:
            splitters.append(in_this_line)
    print("======= splitterS?")
    for idx, x in enumerate(splitters):
        print("========== x", idx, x)

    timelines = explore(splitters, 0, beam)
    return timelines
