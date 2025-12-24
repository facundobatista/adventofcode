import itertools
import re
import sys

#lines = """
##.#.### 1,1,3
#.#...#....###. 1,1,3
#.#.###.#.###### 1,3,1,6
#####.#...#... 4,1,1
##....######..#####. 1,6,5
#.###.##....# 3,2,1
#"""
lines = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()


# for line in lines:
#     cond, annot = line.split()
#     extracted = re.findall(r"(#+)\.*", cond)
#     extlens = [len(x) for x in extracted]
#     print("========", repr(cond), extlens)
#     assert extlens == list(map(int, annot.split(",")))

def _produce_possibilities(srccond):
    qpos = [idx for idx, char in enumerate(srccond) if char == "?"]
    for possib in itertools.product("#.", repeat=len(qpos)):
        cond = list(srccond)
        for pos, char in zip(qpos, possib):
            cond[pos] = char
        yield "".join(cond)

total = 0
for line in lines:
    print("================== :: L", line)
    srccond, annot = line.split()
    annot = list(map(int, annot.split(",")))
    for cond in _produce_possibilities(srccond):
        extracted = re.findall(r"(#+)\.*", cond)
        extlens = [len(x) for x in extracted]
        if extlens == annot:
            print("======== poss", repr(cond), extlens)
            total += 1
print("Total:", total)
