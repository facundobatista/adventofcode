import itertools
from functools import reduce
from operator import xor


test_lines = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""
expected_test_result = 7


def get_pushes(line):
    raw_target, *raw_buttons, _ = line.split()
    print("=========RT", repr(raw_target))

    assert raw_target[0] == "[" and raw_target[-1] == "]"
    raw_target = raw_target[1:-1]
    target_width = len(raw_target)
    target = int(raw_target.replace(".", "0").replace("#", "1"), 2)
    print("======= target", target)

    buttons = []
    for raw_button in raw_buttons:
        assert raw_button[0] == "(" and raw_button[-1] == ")"
        raw_button = raw_button[1:-1]
        butraw_digs = {int(x) for x in raw_button.split(",")}
        print("===== but raw d", butraw_digs)
        butnum_digs = ["1" if x in butraw_digs else "0" for x in range(target_width)]
        print("===== but raw n", butnum_digs)
        button = int("".join(butnum_digs), 2)
        print("===== button", button)
        buttons.append(button)

    qp = 0
    while True:
        qp += 1
        print("========= trying qp", qp)

        # check any combination for the given pushes; first match is enough
        for selected in itertools.combinations(buttons, qp):
            print("===== selected", selected)
            result = reduce(xor, selected, 0)
            print("======= res", result)
            if result == target:
                return qp





def run(lines):
    total = 0
    for line in lines:
        pushes = get_pushes(line)
        total += pushes
    return total
