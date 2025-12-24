import pytest

test_lines = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""
expected_test_result = 6

dial_start = 50
dial_size = 100


def _parse_lines(lines):
    rotations = []
    for line in lines:
        direction, digits = line[0], line[1:]
        quant = int(digits)
        if direction == "L":
            quant *= -1
        rotations.append(quant)
    return rotations


def _count(dial, rot):
    prvdial = dial
    fulls, dial = divmod(dial + rot, dial_size)
    fulls = abs(fulls)
    if rot < 0:
        if dial == 0:
            fulls += 1
        if prvdial == 0:
            fulls -= 1
    return dial, fulls


def run(lines):
    rotations = _parse_lines(lines)
    dial = dial_start
    count = 0
    for rot in rotations:
        dial, fulls = _count(dial, rot)
        count += fulls

    return count


@pytest.mark.parametrize(
    "start,rot,end,count",
    [
        (30, 30, 60, 0),
        (30, 90, 20, 1),
        (30, 70, 0, 1),
        (0, 70, 70, 0),
        (0, 100, 0, 1),
        (30, 170, 0, 2),
        (0, 170, 70, 1),
        (0, 300, 0, 3),
        (30, -10, 20, 0),
        (30, -40, 90, 1),
        (30, -150, 80, 2),
        (30, -30, 0, 1),
        (30, -130, 0, 2),
        (0, -30, 70, 0),
        (0, -130, 70, 1),
        (0, -100, 0, 1),
        (0, -200, 0, 2),
    ]
)
def test_counter(start, rot, end, count):
    realend, realcount = _count(start, rot)
    assert end == realend
    assert count == realcount
