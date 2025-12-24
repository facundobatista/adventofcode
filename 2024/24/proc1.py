import re
import sys

lines = """
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
"""
should_result = 4


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

store = init_wires = []
raw_operations = []
for line in lines:
    if not line:
        store = raw_operations
        continue
    store.append(line)
print("======= init", init_wires)
print("======= ops", raw_operations)

OPS = {
    "OR": "|",
    "AND": "&",
    "XOR": "^",
}

wires = {}
for line in init_wires:
    wire, value = line.split(":")
    wires[wire] = value.strip()

operations = []
for operation in raw_operations:
    src1, op, src2, dst = re.match(r"(\w+) (\w+) (\w+) -> (\w+)", operation).groups()
    operations.append((src1, op, src2, dst))


# operations are in bad order; so let's consume them while we can, until we exhaust them
while operations:
    item = operations.pop(0)
    src1, op, src2, dst = item
    print("==== op", src1, op, src2, dst)
    v1 = wires.get(src1)
    v2 = wires.get(src2)
    if v1 is None or v2 is None:
        # missing info
        print("======== MISSING")
        operations.append(item)
    else:
        # we're ok
        realop = OPS[op]
        built = f"({v1} {realop} {v2})"
        wires[dst] = built
    print("==== w??", wires)

z_wires = [(k, eval(v)) for k, v in sorted(wires.items()) if k[0] == "z"]
print("======== z wires", z_wires)

total = 0
for idx, (zw, val) in enumerate(z_wires):
    print("==== zw", idx, zw, val)
    total += val * 2 ** idx


print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
