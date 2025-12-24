import itertools
import math
from collections import Counter

test_lines = """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""
expected_test_result = 40

connections_limit = 1000


def _parse_lines(lines):
    lines = [x.split(",") for x in lines]
    lines = [tuple(map(int, item)) for item in lines]
    return lines


def run(lines):
    lines = _parse_lines(lines)

    # precalculate distances, and order starting from lower
    measured = []
    for j1, j2 in itertools.combinations(lines, 2):
        d = math.sqrt((j1[0] - j2[0]) ** 2 + (j1[1] - j2[1]) ** 2 + (j1[2] - j2[2]) ** 2)
        measured.append((d, j1, j2))
    measured.sort()
    print("======== m", measured[:3])
    measured[connections_limit:] = []

    circuits = {}
    cn = 0
    for _, j1, j2 in measured:
        circ1 = circuits.get(j1)
        circ2 = circuits.get(j2)
        print("========== indiv circs:", circ1, circ2)
        if circ1 is None and circ2 is None:
            # new circuit!
            circuits[j1] = cn
            circuits[j2] = cn
            cn += 1
        elif circ1 is not None and circ2 is None:
            circuits[j2] = circ1
        elif circ1 is None and circ2 is not None:
            circuits[j1] = circ2
        elif circ1 == circ2:
            pass  # both already in the same circuit, nothing happens
        else:
            # two different circuits, move all from second circuit to the first one
            for j, c in circuits.items():
                if c == circ2:
                    circuits[j] = circ1
        # print("========== circuits", circuits)

    print("========== final circuits", circuits)
    circs = set(circuits.values())
    for c in sorted(circs):
        print("======= C", c, len([k for k, v in circuits.items() if v == c]))

    # sizes
    quants = Counter(circuits.values())
    top3 = quants.most_common(3)
    print("========= top 3", top3)

    result = 1
    for _, q in top3:
        result *= q

    return result
