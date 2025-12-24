import sys

lines = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()


def is_safe(line):
    nums = [int(x) for x in line.split()]
    print("==== N", nums)
    decreasing = (nums[0] - nums[1]) > 0
    nums2 = iter(nums)
    next(nums2)

    for n1, n2 in zip(nums, nums2):
        print("===== n1, n2", n1, n2)
        diff = n1 - n2
        if decreasing and diff < 0:
            return False
        if not decreasing and diff > 0:
            return False
        if not (1 <= abs(diff) <= 3):
            return False
    return True


total = sum(is_safe(line) for line in lines)
print("Total:", total)
