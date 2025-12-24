import sys

lines = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

lines = """
24 21 22 24 25 26 27
"""


if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()


def is_safe(nums):

    d1 = 1 if (nums[0] - nums[1]) > 0 else -1
    d2 = 1 if (nums[1] - nums[2]) > 0 else -1
    d3 = 1 if (nums[2] - nums[3]) > 0 else -1
    decreasing = sum((d1, d2, d3)) > 0
    print("==== Dec?", decreasing)

    nums2 = iter(nums)
    next(nums2)

    for idx, (n1, n2) in enumerate(zip(nums, nums2)):
        print("===== n1, n2", n1, n2)
        diff = n1 - n2
        if decreasing and diff < 0:
            return idx
        if not decreasing and diff > 0:
            return idx
        if not (1 <= abs(diff) <= 3):
            return idx
    return None


total = 0
for line in lines:
    nums = [int(x) for x in line.split()]
    print("\n======== N", nums)
    result = is_safe(nums)
    if result is None:
        # great!
        print("=== ok de una")
        total += 1
        continue

    # result is the idx of where problem is detected, try without one or the other
    idx = result
    new_nums = nums.copy()
    removed = new_nums.pop(idx)
    print(f"===== removed first problematic ({idx}) {removed}")
    result = is_safe(new_nums)
    if result is None:
        print("=== ok de segunda")
        total += 1
        continue
    removed = nums.pop(idx + 1)
    print(f"===== removed second problematic ({idx + 1}) {removed}")
    result = is_safe(nums)
    if result is None:
        print("=== ok de tercera")
        total += 1
    else:
        print("=== unsafe")

print("Total:", total)
