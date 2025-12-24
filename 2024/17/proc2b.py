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


def explore(init_a):
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
    return output


def showgrid(grid):
    for row in grid:
        print("    0o" + "".join(map(str, row)))


positions = len(program)
reversed_program_word = "".join(map(str, reversed(program)))
all_empty = [0] * positions
stack = [(all_empty.copy(), 0)]
succesful = []
while stack:
    seed, column = stack.pop(0)
    print("\nstarting:", column, seed)
    for idx in range(8):
        seed[column] = idx
        if seed == all_empty:
            # special case of 0, don't want
            continue
        print("======= trying", seed)
        code = int("".join(map(str, seed)), 8)
        result = explore(code)
        reverse_result = "".join(map(str, reversed(result[-column-1:])))
        if reverse_result == reversed_program_word:
            # success!
            succesful.append(code)
            print("============== YES")
        else:
            print("============= ?", result, reverse_result, reversed_program_word.startswith(reverse_result))
            if reversed_program_word.startswith(reverse_result):
                stack.append((seed.copy(), column + 1))

print("======== suc?", succesful)
total = min(succesful)

print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
