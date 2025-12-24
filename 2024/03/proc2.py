import re
import sys

lines = """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()


def reduce(line):
    parts = re.findall(r"(mul\(\d{1,3},\d{1,3}\))|(do\(\))|(don't\(\))", line)
    print("==== P", parts)

    # coalesce
    joined = []
    for part in parts:
        (useful,) = [p for p in part if p]
        joined.append(useful)
    print("==== J", joined)

    total = 0
    do_it = True
    for part in joined:
        print("======== J?", repr(part))
        if part.startswith("mul"):
            if do_it:
                m = re.match(r"mul\((\d{1,3}),(\d{1,3})\)", part)
                print("======= X", repr(part), m)
                x, y = map(int, m.groups())
                total += x * y
        elif part == "do()":
            do_it = True
        elif part == "don't()":
            do_it = False
        else:
            raise ValueError()

    return total


total = reduce("".join(lines))
print("Total:", total)

# 87863550 too high
# 83158140 ?
