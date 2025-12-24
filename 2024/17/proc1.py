import re
import sys

lines = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""
should_result = "4,6,3,5,6,3,5,2,1,0"


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
OUTPUT = []


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


def adv(operand):
    numerator = Reg.A
    denominator = 2 ** combo(operand)
    Reg.A = numerator // denominator


def bxl(operand):
    Reg.B = Reg.B ^ operand


def bst(operand):
    Reg.B = combo(operand) % 8


def jnz(operand):
    if Reg.A:
        return operand


def bxc(operand):
    Reg.B = Reg.B ^ Reg.C


def out(operand):
    OUTPUT.append(combo(operand) % 8)


def bdv(operand):
    numerator = Reg.A
    denominator = 2 ** combo(operand)
    Reg.B = numerator // denominator


def cdv(operand):
    numerator = Reg.A
    denominator = 2 ** combo(operand)
    Reg.C = numerator // denominator


FUNCS = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]

pc = 0
while pc < len(program):
    opcode, operand = program[pc:pc + 2]
    print("===== opcode, operand", opcode, operand)
    func = FUNCS[opcode]
    new_pc = func(operand)
    if new_pc is None:
        pc += 2
    else:
        pc = new_pc


total = ",".join(map(str, OUTPUT))
print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
