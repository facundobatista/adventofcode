import re
import sys
from collections import deque

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
should_result = 2024

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
print("======= init", init_wires_raw)
print("======= ops", raw_operations)

OPS = {
    "OR": "|",
    "AND": "&",
    "XOR": "^",
}

init_wires = {}
for line in init_wires_raw:
    wire, value = line.split(":")
    init_wires[wire] = value.strip()

operations = deque()
for operation in raw_operations:
    src1, op, src2, dst = re.match(r"(\w+) (\w+) (\w+) -> (\w+)", operation).groups()
    realop = OPS[op]
    operations.append((src1, realop, src2, dst))


def get_num(letter, wires):
    letter_wires = [(k, eval(v)) for k, v in sorted(wires.items()) if k[0] == letter]

    total = 0
    for idx, (letw, val) in enumerate(letter_wires):
        total += val * 2 ** idx
    return total


def process(operations, wires):
    # operations are in bad order; so let's consume them while we can, until we exhaust them
    while operations:
        item = operations.popleft()
        src1, op, src2, dst = item
        # print("==== op", src1, op, src2, dst)
        v1 = wires.get(src1)
        v2 = wires.get(src2)
        if v1 is None or v2 is None:
            # missing info
            # print("======== MISSING")
            operations.append(item)
        else:
            # we're ok
            built = f"({v1} {op} {v2})"
            wires[dst] = built
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
#should_result = x_num + y_num
print("========= should?", should_result)

val = process(operations, init_wires)
print("========= val?", val, val == should_result)



print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
