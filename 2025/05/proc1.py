from advent_utils import get_blocks

test_lines = """
3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""
expected_test_result = 3


def run(lines):
    fresh_ranges, available = get_blocks(lines)
    print("====== fres", fresh_ranges)
    available = [int(a) for a in available]
    print("======= avao", available)

    fresh_ids = []
    for fresh_range in fresh_ranges:
        rf, rt = map(int, fresh_range.split("-"))
        fresh_ids.append(range(rf, rt + 1))
    print("====== fresh ids", fresh_ids)

    total = 0
    for ingredient in available:
        if any(ingredient in rng for rng in fresh_ids):
            total += 1

    return total
