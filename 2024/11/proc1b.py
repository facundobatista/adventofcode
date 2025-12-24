import math
import sys
from functools import cache

lines = """
0 1 10 99 999
"""
total_blinks = 75

# total_blinks = 30
# Total: 1012184
# real    0m0,193s


# total_blinks = 40
# Total: 66177948
# real    0m7,638s


# lines = """
#     125 17
# """
# total_blinks = 6
# total_blinks = 25

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()


class Node:
    __slots__ = ("stone", "children")

    cached = {}

    def __init__(self, stone):
        self.stone = stone
        self.children = []

    def born(self, *new_stones):
        new_nodes = []
        for stone in new_stones:
            if stone in self.cached:
                old_node = self.cached[stone]
                self.children.append(old_node)
            else:
                new_node = Node(stone)
                self.cached[stone] = new_node
                self.children.append(new_node)
                new_nodes.append(new_node)

        return new_nodes

    def __repr__(self):
        return f"Node({self.stone}, {self.children})"


assert len(lines) == 1
stones = [int(x) for x in lines[0].split()]
roots = [Node(stone) for stone in stones]
Node.cached.update({node.stone: node for node in roots})

to_process_nodes = roots
for blink in range(total_blinks):
    print("======= blink", blink, len(to_process_nodes))
    if not to_process_nodes:
        break

    new_nodes = []
    for node in to_process_nodes:
        if node.stone == 0:
            new_nodes.extend(node.born(1))
            continue

        ql = int(math.log10(node.stone))
        lesshalf, rest = divmod(ql, 2)
        if rest == 1:  # we're flooring the logarithm
            # even number of digits
            left_stone, right_stone = divmod(node.stone, 10 ** (lesshalf + 1))
            new_nodes.extend(node.born(left_stone, right_stone))
            continue

        new_nodes.extend(node.born(node.stone * 2024))

    to_process_nodes = new_nodes


def show(node, level):
    print("    " * level, node.stone)

    level += 1
    if level == total_blinks:
        print("    " * level, "done", [node.stone for node in node.children])
        return

    for node in node.children:
        show(node, level)


# print("-----------------------------------")
# for node in roots:
#     show(node, 0)
# print("-----------------------------------")


@cache
def walk(node, level):
    level += 1
    if level == total_blinks:
        return len(node.children)

    if not node.children:
        # branch end, this is the last node
        return 1

    added = 0
    for node in node.children:
        added += walk(node, level)
    return added


print(f"Walk {len(roots)} roots")
total = 0
for node in roots:
    print("========= root", node.stone)
    total += walk(node, 0)
print("Total:", total)
