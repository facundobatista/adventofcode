import itertools

test_lines = """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""
expected_test_result = 50


def _parse_lines(lines):
    lines = [x.split(",") for x in lines]
    lines = [tuple(map(int, item)) for item in lines]
    return lines


def run(lines):
    lines = _parse_lines(lines)

    maxarea = 0
    for c1, c2 in itertools.combinations(lines, 2):
        w = abs(c1[0] - c2[0]) + 1
        h = abs(c1[1] - c2[1]) + 1
        area = w * h
        maxarea = max(area, maxarea)

    return maxarea
