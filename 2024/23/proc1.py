import sys
from itertools import combinations

lines = """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""
should_result = 7

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
    should_result = None
else:
    print("Bad arg")
    exit()

#
# aq
# wq cg vc yn
#
# wq
# tb ub aq vc
#
# tb
# cg ka wq vc
#
# ub
# qp kh wq vc
#
# vc
# aq ub wq tb
#
#
# ---
#
#
# kh-tc qp-kh de-cg
# vc-aq vc-wq wq-aq
#

splitted = [x.split("-") for x in lines]
with_t = [p for p in splitted if p[0][0] == "t" or p[1][0] == "t"]
without_t = [p for p in splitted if p[0][0] != "t" and p[1][0] != "t"]
print("========= Ty", len(with_t))
print("========= Tn", len(without_t))


def supercomb():
    for x in combinations(with_t, 3):
        yield x
    for x in combinations(with_t, 2):
        for y in without_t:
            yield x[0], x[1], y
    for x in with_t:
        for y in combinations(without_t, 2):
            yield x, y[0], y[1]

total = 0
for idx, trip in enumerate(supercomb()):
    if idx % 1000000 == 0:
        print("======== raw", idx, trip)
    s = set()
    for x in trip:
        s.update(x)
    if len(s) == 3:
        total += 1

print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
