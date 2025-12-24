import itertools
import re
import sys

lines = """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""


if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()

# load everything
lines = iter(lines)
trad = {"L": 0, "R": 1}
instructions = itertools.cycle([trad[c] for c in next(lines).strip()])
assert next(lines).strip() == ""
nodes = {}
for line in lines:
    src, dst1, dst2 = re.match(r"(\w\w\w) = \((\w\w\w), (\w\w\w)\)", line).groups()
    nodes[src] = (dst1, dst2)
print("==== nodes", nodes)

node = "AAA"
count = 0
for inst in instructions:
    node = nodes[node][inst]
    count += 1
    print("====== n", node)
    if node == "ZZZ":
        break
print("Steps:", count)
