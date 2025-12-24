import sys

lines = """
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""
should_result = 3


if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
    should_result = None
else:
    print("Bad arg")
    exit()

blocks = []
curblock = []
for line in lines:
    line = line.strip()
    if not line:
        blocks.append(curblock)
        curblock = []
    else:
        curblock.append(line)
blocks.append(curblock)
print("====== len(blocks)", len(blocks))

# locks
# 0, 5, 3, 4, 3
# 1, 2, 0, 5, 3
# ->
#     5, 0, 2, 1, 2
#     4, 3, 5, 0, 2
#
# keys
# 5, 0, 2, 1, 3
# 4, 3, 4, 0, 2
# 3, 0, 2, 0, 1

# separate each block in locks (inverted) and keys
locks = []
keys = []
for block in blocks:
    first, *middle, last = block
    if first == "#####" and last == ".....":
        heights = [5 - row.count("#") for row in zip(*middle)]
        locks.append(heights)
    elif first == "....." and last == "#####":
        heights = [row.count("#") for row in zip(*middle)]
        keys.append(heights)
    else:
        raise ValueError("bad block")
print("======= L", locks)
print("======= K", keys)

total = 0
for lock in locks:
    for key in keys:
        print("====== l", lock)
        print("====== k", key)
        if all(lv >= kv for lv, kv in zip(lock, key)):
            print("======== YES")
            total += 1


print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
