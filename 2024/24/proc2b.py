import re
import sys
from collections import deque
from itertools import combinations

lines = """
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
"""

# lines = """
# x00: 1
# x01: 1
# x02: 1
# y00: 0
# y01: 1
# y02: 0
#
# x00 OR y00 -> z03
# x01 XOR y01 -> z02
# x02 AND y02 -> z01
# x02 OR y02 -> z00
# """

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
    should_result = None
else:
    print("Bad arg")
    exit()

store = init_wires_raw = []
raw_operations = []
for line in lines:
    if not line:
        store = raw_operations
        continue
    store.append(line)
print("======= ops", raw_operations)
# sort in reverse so x and y are first
raw_operations.sort(reverse=True)

init_wires = {}
for line in init_wires_raw:
    wire, value = line.split(":")
    init_wires[wire] = int(value.strip())
print("======= init", init_wires)

operat_lefts = deque()
operat_rights = deque()
for operation in raw_operations:
    src1, op, src2, dst = re.match(r"(\w+) (\w+) (\w+) -> (\w+)", operation).groups()
    operat_lefts.append((src1, op, src2))
    operat_rights.append(dst)


def get_num(letter, wires):
    letter_wires = [(k, v) for k, v in sorted(wires.items()) if k[0] == letter]

    total = 0
    for idx, (letw, val) in enumerate(letter_wires):
        total += val * 2 ** idx
    return total


def process(operat_lefts, operat_rights, wires):
    # operations are in bad order; so let's consume them while we can, until we exhaust them
    indexes = deque(range(len(operat_rights)))
    prv_size = len(indexes)
    counter = 0
    while indexes:
        index_size = len(indexes)
        if prv_size != index_size:
            counter = 0
            prv_size = index_size
        # print("====== index cnt", index_size, counter, indexes)
        if counter == index_size:
            return -1
        counter += 1

        idx = indexes.popleft()
        src1, op, src2 = operat_lefts[idx]
        # print("========= src?", src1, src2)
        v1 = wires.get(src1)
        v2 = wires.get(src2)
        if v1 is None or v2 is None:
            # missing info
            # print("======== MIS")
            indexes.append(idx)
        else:
            # we're ok
            if op == "AND":
                res = v1 & v2
            elif op == "OR":
                res = v1 | v2
            else:
                res = v1 ^ v2
            dst = operat_rights[idx]
            wires[dst] = res
        # print("==== w??", wires)

    return get_num("z", wires)


# 222 operations
# >>> len(list(combinations("x" * 222, 4)))
# 98491965
# >>> l * .01 / 3600
# 273.5887916666667

# what should we get?
x_num = get_num("x", init_wires)
y_num = get_num("y", init_wires)
should_result = x_num + y_num
print("========= should?", should_result)
val = process(operat_lefts, operat_rights, init_wires.copy())
print("=== no swap", val)


def hipercombine():
    wire_positions = list(range(len(operat_rights)))
    for a, b in combinations(wire_positions, 2):
        subw1 = [x for x in wire_positions if x != a and x != b]
        for c, d in combinations(subw1, 2):
            subw2 = [x for x in subw1 if x != c and x != d]
            for e, f in combinations(subw2, 2):
                subw3 = [x for x in subw2 if x != e and x != f]
                for g, h in combinations(subw3, 2):
                    yield a, b, c, d, e, f, g, h


for ws0, wd0, ws1, wd1, ws2, wd2, ws3, wd3 in hipercombine():
    print("====== swaps", ws0, wd0, ws1, wd1, ws2, wd2, ws3, wd3)
    operat_rights[ws0], operat_rights[wd0] = operat_rights[wd0], operat_rights[ws0]
    operat_rights[ws1], operat_rights[wd1] = operat_rights[wd1], operat_rights[ws1]
    operat_rights[ws2], operat_rights[wd2] = operat_rights[wd2], operat_rights[ws2]
    operat_rights[ws3], operat_rights[wd3] = operat_rights[wd3], operat_rights[ws3]
    # print("======= rights", operat_rights)

    val = process(operat_lefts, operat_rights, init_wires.copy())

    operat_rights[ws0], operat_rights[wd0] = operat_rights[wd0], operat_rights[ws0]
    operat_rights[ws1], operat_rights[wd1] = operat_rights[wd1], operat_rights[ws1]
    operat_rights[ws2], operat_rights[wd2] = operat_rights[wd2], operat_rights[ws2]
    operat_rights[ws3], operat_rights[wd3] = operat_rights[wd3], operat_rights[ws3]
    # print("======= val", val)
    if val == should_result:
        break
else:
    print("Booo")
    exit()

swapped = []
for pos in ws0, wd0, ws1, wd1, ws2, wd2, ws3, wd3:
    swapped.append(operat_rights[pos])
total = ",".join(swapped)

print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
