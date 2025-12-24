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
should_result = 16

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

root = {}
for src in sources:
    node = root
    for c in src:
        node = node.setdefault(c, {})
    node[None] = None


def check(idx, design):
    print("\n============= MASTER", design, f"{idx}/{len(designs)}")
    stack = [(root, 0)]
    count = 0
    len_design = len(design)
    while stack:
        node, pos = stack.pop()
        next_pos = pos + 1
        if next_pos > len_design:
            # this is the end; if letter in the node and it was the end of a word, it's ok!
            if None in node:
                count += 1
            continue

        char = design[pos]
        if char in node:
            stack.append((node[char], next_pos))
        if None in node and char in root:
            stack.append((root[char], next_pos))

    return count


total = sum(check(idx, design) for idx, design in enumerate(designs, 1))
print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
