import re
import sys

lines = """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()


def reduce(line):
    parts = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", line)
    print("==== P", parts)
    return sum(int(x) * int(y) for x, y in parts)


total = reduce("".join(lines))
assert total == 173785482
print("Total:", total)
