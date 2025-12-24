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
# print("==== nodes", nodes)

# curnodes = [n for n in nodes if n[2] == "A"]
# print("==== start", curnodes)
# count = 0
# for inst in instructions:
#     curnodes = [nodes[node][inst] for node in curnodes]
#     count += 1
#     print("======= cur", count, curnodes)
#     if all(n[2] == "Z" for n in curnodes):
#         break
# print("Steps:", count)

startnodes = [n for n in nodes if n[2] == "A"]

print("==== start", startnodes)
sequences = []
for thisnode in startnodes:
    startingnodes = {}
    seq = []
    while True:
        print("==== starting", thisnode)
        startingnodes[thisnode] = len(seq)
        for inst in instructions:
            seq.append(thisnode)
            thisnode = nodes[thisnode][inst]
        print("==== endedint", thisnode)
        if thisnode in startingnodes:
            break

    print("==== sss seq", seq)
    start = startingnodes[thisnode]
    print("==== sss str", start)
    sequences.append((start, seq))

for s in sequences:
    print("raw seqs", s)

all_with_z = []
for start, seq in sequences:
    prevrep = seq[:start]
    prev_with_z = [idx for idx, node in enumerate(prevrep) if node[2] == "Z"]
    postrep = seq[start:]
    post_with_z = [idx for idx, node in enumerate(postrep) if node[2] == "Z"]

    all_with_z.append((prev_with_z, post_with_z, start, len(seq) - start))

for x in all_with_z:
    print("with z::", x)
breakpoint()
21409, 21680, 21951, 22222
21409 * 14363 * 15989 * 16531 * 19241 * 19783

all_pos = []
for lotwithz, rep_with_z, start, rep_l in all_with_z:
    base = start
    while len(lotwithz) < 100:
        for wz in rep_with_z:
            lotwithz.append(base + wz)
        base += rep_l
    all_pos.append(lotwithz)

for x in all_pos:
    print("the pos:", x)

setpos = set(all_pos[0])
for pos in all_pos[1:]:
    setpos &= set(pos)
print("Step:", min(setpos))

