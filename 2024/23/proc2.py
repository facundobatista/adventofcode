import sys

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
should_result = "co,de,ka,ta"

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
    should_result = None
else:
    print("Bad arg")
    exit()

splitted = [x.split("-") for x in lines]
nodes = {}
for na, nb in splitted:
    nodes.setdefault(na, []).append(nb)
    nodes.setdefault(nb, []).append(na)

print("========= nodes", nodes)

# ka
# co tb ta de
#
#     co
#     ka ta de tc
#       -- no ka (viene de ahí)
#       -- queda ta,de,tc
#
#         ta
#         co ka de kh
#           -- no co (viene de ahi) y tampoco ka (validar)
#           -- queda de,kh
#
#             de
#             cg co ta ka
#               -- no ta (vien de ahí) y tampoco ka, co (validar)
#               -- queda cg
#
#               cg
#               de tb yn aq
#                 -- no de (viene de ahí) y FALLA VALIDACION ACÁ FRENA
#
#             kh
#             tc, qp, ub, ta
#               -- no ta (viene de ahí) y FALLA
#
#         tc
#         kh wh td co


def walk(node):
    repo = set()
    stack = [node]
    while stack:
        print("======= loop, repo", repo)
        print("======= loop, stck", stack)
        node = stack.pop()
        print("======= insp", repr(node))
        subs = set(nodes[node])
        print("======= subs", subs)

        if not repo.issubset(subs):
            print("============ FAIL")
            continue
        repo.add(node)

        usfs = subs - repo
        print("======= usfs", usfs)
        stack.extend(usfs)
    return repo


combos = []
for startnode in nodes:
    repo = walk(startnode)
    print("======== startn", repo)
    combos.append(repo)

largest = max(combos, key=len)
total = ",".join(sorted(largest))

print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
