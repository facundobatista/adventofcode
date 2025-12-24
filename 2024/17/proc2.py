import re
import sys

lines = """
Register A: 2440
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""
should_result = 117440


if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
    should_result = None
else:
    print("Bad arg")
    exit()


class Reg:
    pass


for line in lines:
    line = line.strip()
    if line.startswith("Reg"):
        name, value = re.match(r"Register (.): (\d+)", line).groups()
        setattr(Reg, name, int(value))
    elif line.startswith("Prog"):
        program = [int(x) for x in line.split()[1].split(",")]

print("========= registers", Reg.A, Reg.B, Reg.C)
print("========= program", program)


def combo(value):
    if 0 <= value <= 3:
        return value
    if value == 4:
        return Reg.A
    if value == 5:
        return Reg.B
    if value == 6:
        return Reg.C
    raise ValueError("Invalid combo value")


prefix = program[-2::-1]  # skip first, the rest reversed
digs_from = prefix + [0]
digs_to = prefix + [7]
num_from = int("".join(map(str, digs_from)), 8)
num_to = int("".join(map(str, digs_to)), 8)

#lp = len(program) - 1
#for init_a in range(8 ** lp, 8 ** (lp + 1)):

#hc_f = 0o1000000000000000
#hc_t = 0o1000000010000000
#for init_a in range(hc_f, hc_t):

hclist = [
    0o1000000000000000,
    0o2000000000000000,
    0o3000000000000000,
    0o4000000000000000,
    0o5000000000000000,
    0o6000000000000000,
    0o7000000000000000,

    # 0o5000000000000000,
    # 0o5100000000000000,
    # 0o5200000000000000,
    # 0o5300000000000000,
    # 0o5400000000000000,
    # 0o5500000000000000,
    # 0o5600000000000000,
    # 0o5700000000000000,
    #
    # 0o5600000000000000,
    # 0o5610000000000000,
    # 0o5620000000000000,
    # 0o5630000000000000,
    # 0o5640000000000000,
    # 0o5650000000000000,
    # 0o5660000000000000,
    # 0o5670000000000000,
]
for init_a in hclist:

#for init_a in range(num_from, num_to + 1):

    Reg.A = init_a
    pc = 0
    output = []
    while pc < len(program):
        opcode, operand = program[pc:pc + 2]
        pc += 2  # may be overriden by operation

        if opcode == 0:
            numerator = Reg.A
            denominator = 2 ** combo(operand)
            Reg.A = numerator // denominator
        elif opcode == 1:
            Reg.B = Reg.B ^ operand
        elif opcode == 2:
            Reg.B = combo(operand) % 8
        elif opcode == 3:
            if Reg.A:
                pc = operand
        elif opcode == 4:
            Reg.B = Reg.B ^ Reg.C
        elif opcode == 5:
            output.append(combo(operand) % 8)
        elif opcode == 6:
            numerator = Reg.A
            denominator = 2 ** combo(operand)
            Reg.B = numerator // denominator
        elif opcode == 7:
            numerator = Reg.A
            denominator = 2 ** combo(operand)
            Reg.C = numerator // denominator
        else:
            raise ValueError("Bad opcode")

    print("========== A?", init_a, oct(init_a), output)
    if output == program:
        total = init_a
        break
else:
    total = None

print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
