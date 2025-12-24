import functools
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
cache = {}


def walk(haystack, pos=0):
    step = pos * "    "
    # print(step, "=========== walk", haystack)
    if haystack in cache:
        # print(step, "======= cached", cache[haystack])
        return cache[haystack]

    count = 0
    for src in sources:
        # print(step, "=========== loop", (haystack, src))
        if haystack == src:
            # reached the end!
            # print(step, "=========== END")
            count += 1
        if haystack.startswith(src):
            # print(step, "=========== yes!!")
            sub = walk(haystack[len(src):], pos + 1)
            # print(step, "=========== got", sub)
            count += sub

    cache[haystack] = count
    return count


def check(idx, design):
    print("============= MASTER", design, f"{idx}/{len(designs)}")
    count = walk(design)
    print("=============== final", count)
    return count


total = sum(check(idx, design) for idx, design in enumerate(designs, 1))
print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
