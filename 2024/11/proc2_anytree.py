import math
import sys

lines = """
0 1 10 99 999
"""
total_blinks = 75
total_blinks = 30

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
    __slots__ = ("holder", "idx", "stone")

    def __init__(self, holder, idx, stone):
        self.holder = holder
        self.idx = idx
        self.stone = stone

    def set(self, new_stone):
        self.stone = new_stone

    def split(self, left, right):
        self.holder[self.idx] = holder = []
        holder.extend((
            Node(holder, 0, left),
            Node(holder, 1, right),
        ))

    def __repr__(self):
        return f"Node({self.stone})"


assert len(lines) == 1
stones = [int(x) for x in lines[0].split()]
root_holder = []
root_holder.extend(Node(root_holder, idx, stone) for idx, stone in enumerate(stones))


def walk(holder):
    stack = [iter(holder)]

    while stack:
        try:
            node = next(stack[-1])
            if isinstance(node, list):
                stack.append(iter(node))
            else:
                yield node
        except StopIteration:
            stack.pop()


for blink in range(total_blinks):
    print("======= blink", blink)

    for node in walk(root_holder):
        if node.stone == 0:
            node.set(1)
            continue

        ql = int(math.log10(node.stone))
        lesshalf, rest = divmod(ql, 2)
        if rest == 1:  # we're flooring the logarithm
            # even number of digits
            left_stone, right_stone = divmod(node.stone, 10 ** (lesshalf + 1))
            node.split(left_stone, right_stone)
            continue

        node.set(node.stone * 2024)


# for blink in range(total_blinks):
#     print("======= seq", blink, len(stones))
#
#     new_stones = []
#     for stone in stones:
#         if stone == 0:
#             new_stones.append(1)
#             continue
#
#         ql = int(math.log10(stone))
#         lesshalf, rest = divmod(ql, 2)
#         if rest == 1:  # we're flooring the logarithm
#             # even number of digits
#             left_stone, right_stone = divmod(stone, 10 ** (lesshalf + 1))
#             new_stones.append(left_stone)
#             new_stones.append(right_stone)
#             continue
#
#         new_stones.append(stone * 2024)
#
#     stones = new_stones


print("Total:", len(list(walk(root_holder))))
