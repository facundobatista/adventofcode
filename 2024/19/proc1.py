import sys

lines = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""
should_result = 6

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
    should_result = None
else:
    print("Bad arg")
    exit()

sources = [x.strip() for x in lines[0].split(",")]
designs = lines[2:]


def check(idx, design):
    print("============= MASTER", design, f"{idx}/{len(designs)}")
    stack = [design]
    while stack:
        design = stack.pop()
        print("=========== sub", design)
        for src in sources:
            if design == src:
                # reached the end!
                return True
            if design.startswith(src):
                print("=========== yes", repr(src))
                stack.append(design[len(src):])

    return False


total = sum(check(idx, design) for idx, design in enumerate(designs, 1))
print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
