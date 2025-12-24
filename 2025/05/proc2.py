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
expected_test_result = 14

# a case with a smaller stop when merging
test_lines = """
3-5
10-14
16-20
12-18
17-19

-
"""


def run(lines):
    fresh_ranges, _ = get_blocks(lines)
    print("====== fres", fresh_ranges)
    ranges = sorted([int(x) for x in fresh_range.split("-")] for fresh_range in fresh_ranges)
    print("========== rngs", ranges)

    merged = []
    prev_start, prev_end = ranges[0]
    for cur_start, cur_end in ranges[1:]:
        print("============ loop", (prev_start, prev_end), (cur_start, cur_end))
        if cur_start <= prev_end:
            # overlapped, just expand current until the largest end
            print("============= OVERLAP")
            prev_end = max(cur_end, prev_end)
        else:
            # disjoint, store old one and continue
            print("============= STORE")
            merged.append((prev_start, prev_end))
            prev_start, prev_end = cur_start, cur_end
    merged.append((prev_start, prev_end))

    print("====== done!", merged)
    total = 0
    for rs, re in merged:
        total += (re + 1 - rs)
    return total


# def run(lines):
#     fresh_ranges, _ = get_blocks(lines)
#     print("====== fres", fresh_ranges)
#
#     expanded = []
#     for fresh_range in fresh_ranges:
#         rf, rt = map(int, fresh_range.split("-"))
#         newrng = range(rf, rt + 1)
#         print("========================== new range!", newrng)
#         if not expanded:
#             expanded.append(newrng)
#             continue
#
#         done = False
#         while not done:
#             print("======= loopini", expanded)
#             for idx, oldrng in enumerate(expanded):
#                 new_start_in = newrng.start in oldrng
#                 new_stop_in = newrng.stop in oldrng
#
#                 if new_start_in and new_stop_in:
#                     # new range is completely inside old range, we're done searching
#                     done = True
#                     break
#
#                 if not new_start_in and not new_stop_in:
#                     # new range absorbs the old range, replace and flag to continue
#                     expanded[idx] = newrng
#                     break
#
#                 if new_start_in and not new_stop_in:
#                     # new range starts in the middle of the old but finishes outside, expand
#                     # the old's stop
#                     newrng = range(oldrng.start, newrng.stop)
#                     expanded[idx] = newrng
#
#                     if newrng.stop in oldrng:
#                         # new range is completely inside old range; just discard this new one
#                         break
#                     else:
#                         newrng = range(oldrng.start, newrng.stop)
#                         expanded[idx] = newrng
#                         break
#
#                 # here we already new the start was not inside old range...
#                 if newrng.stop in oldrng:
#                     newrng = range(newrng.start, newrng.stop)
#                     expanded[idx] = newrng
#                     break
#
#
#             if not processed:
#                 expanded.append(newrng)
#                 break
#
#     print("====== expanded", expanded)
#
#     return total
