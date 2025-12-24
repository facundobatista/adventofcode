from safe_map import SafeMap

test_lines = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""
expected_test_result = 43

MARK_ROLL = "@"
MARK_EMPTY = "."


def _get_rolls_around(smap, x, y):
    count = 0
    for dx, dy in smap.ALL_DELTAS:
        nx = x + dx
        ny = y + dy
        space = smap[(nx, ny)]
        if space == MARK_ROLL:
            count += 1
    return count


def run(lines):
    smap = SafeMap(lines, out_of_map=None)
    total = 0
    print("====== pre", smap.show())
    while True:
        thispass = 0
        for x, y, val in smap.walk():
            if val == MARK_ROLL:
                around = _get_rolls_around(smap, x, y)
                if around < 4:
                    thispass += 1
                    smap[(x, y)] = "x"
        print("====== aft", smap.show())
        print("==== thisp", thispass)
        total += thispass
        if thispass == 0:
            break
    return total
