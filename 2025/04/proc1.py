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
expected_test_result = 13

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
    for x, y, val in smap.walk():
        if val == MARK_ROLL:
            print("======= rollo", x, y)
            around = _get_rolls_around(smap, x, y)
            print("========== ar", around)
            if around < 4:
                total += 1
    return total
