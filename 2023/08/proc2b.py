import itertools
import math
import re
import sys

lines = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
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
instructions = [trad[c] for c in next(lines).strip()]
assert next(lines).strip() == ""
nodes = {}
for line in lines:
    src, dst1, dst2 = re.match(r"(\w\w\w) = \((\w\w\w), (\w\w\w)\)", line).groups()
    nodes[src] = (dst1, dst2)

starting_nodes = [n for n in nodes if n[2] == "A"]
print("==== start", starting_nodes)

loops = []
for node in starting_nodes:

    steps = 0
    firstfound = None
    for inst in itertools.cycle(instructions):
        steps += 1
        if node[2] == "Z":
            if firstfound is None:
                firstfound = steps
            else:
                # second time! register the loop and we're done with this node
                loops.append(steps - firstfound)
                break

        node = nodes[node][inst]

total_steps = 1
for c in loops:
    total_steps = math.lcm(c, total_steps)
print("Steps:", total_steps, "ok" if total_steps == 21165830176709 else "MAL")
