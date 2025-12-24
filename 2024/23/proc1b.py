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

splitted = [x.split("-") for x in lines]
allts = set()
nodes = {}
for na, nb in splitted:
    nodes.setdefault(na, []).append(nb)
    nodes.setdefault(nb, []).append(na)
    if na[0] == "t":
        allts.add(na)
    if nb[0] == "t":
        allts.add(nb)

print("========= allts", allts)
print("========= nodes", nodes)

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

combs = set()
# we search for tn-n1, n1-n2, n2-tn
for tnode in allts:
    for node1 in nodes[tnode]:
        for node2 in nodes[node1]:
            if node2 == tnode:
                continue
            for node3 in nodes[node2]:
                if node3 == tnode:
                    print("====== comb!", tnode, node1, node2, node3)
                    comb = tuple(sorted([tnode, node1, node2]))
                    print("====== sort!", comb)
                    combs.add(comb)


total = len(combs)

print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
