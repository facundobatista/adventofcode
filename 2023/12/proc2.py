import re
import sys
from itertools import product

lines = """
.??..??...?##. 1,1,3
?#???..?.#? 2,2,1
??#??????#???.? 4,3
"""
#???.### 1,1,3
#.??..??...?##. 1,1,3
#?#?#?#?#?#?#?#? 1,3,1,6
#????.#...#... 4,1,1
#????.######..#####. 1,6,5
#?###???????? 3,2,1
#"""

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()


def _produce_possibilities(mustcount, srccond):
    qpos = [idx for idx, char in enumerate(srccond) if char == "?"]
    cond = list(srccond)
    for possib in product("#.", repeat=len(qpos)):
        for pos, char in zip(qpos, possib):
            cond[pos] = char
        if cond.count("#") != mustcount:
            continue
        yield "".join(cond)


def _match_blocks(annots, blocks, sofar=[]):
    prefix = "====" * len(sofar)
    print(prefix, "==== match sofar", sofar)
    print(prefix, "==== match annots", annots)
    print(prefix, "==== match blocks", blocks)
    if not blocks:
        # print("==============+ NO MORE")
        yield sofar
        return

    next_block = blocks[0]
    lenblock = len(next_block)

    sumann = 0
    for idx, annot in enumerate(annots):
        sumann += annot
        if sumann >= lenblock:
            break
        sumann += 1  # needed separator if more than one annotation is taken
    thisannots = annots[:idx + 1]
    print(prefix, "===== idx, thisannots", idx, thisannots)

    for idx in range(len(thisannots) + 1):
        yield from _match_blocks(annots[idx:], blocks[1:], sofar + [(annots[:idx], next_block)])


total = 0
regex = re.compile(r"(#+)\.*")
for line in lines:
    print("================== :: L", line)
    srccond, annots = line.split()

    # # unfold
    # srccond = "?".join([srccond] * 5)
    # annots = ",".join([annots] * 5)
    # print("================== :: A", (srccond, annots))

    annots = list(map(int, annots.split(","))) + [0] * 50
    annotcount = sum(annots)
    blocks = [x for x in srccond.split(".") if x]

    totline = 0
    for coupled in _match_blocks(annots, blocks):
        print("============= XXX", coupled)
        totalused = sum(sum(a) for a, b in coupled)
        # print("============ total used", totalused)
        if totalused != annotcount:
            continue
        # print("================= UUUUUUUUU TIL", coupled)

        allpossibs = []
        for c_annots, c_block in coupled:
            if not c_annots and "#" not in c_block:
                continue
            cancount = sum(c_annots)
            # print("===============    = ========= block", c_block)

            newposs = []
            for possib in _produce_possibilities(cancount, c_block):
                parts = regex.findall(possib)
                # print("============???", parts, c_annots)
                if [len(p) for p in parts] == c_annots:
                    # print("===============    = =========  -- real!!!", possib)
                    newposs.append(possib)

            allpossibs.append(newposs)

        # print("================= UUUUUU SIRVE?", allpossibs)
        totseq = 1
        for possib in allpossibs:
            totseq *= len(possib)
        print("================= UUUUUU totseq", totseq)
        totline += totseq
    # print("================== :: v", totline)
    total += totline

print("Total:", total, "ok" if total == 7191 else "MAL")
