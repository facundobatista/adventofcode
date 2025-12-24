import math


class Node:
    __slots__ = ("holder", "idx", "stone")

    def __init__(self, holder: list, idx: int, stone: int):
        self.holder = holder
        self.idx = idx
        self.stone = stone

    def set(self, new_stone: int):
        self.stone = new_stone

    def split(self, left: int, right: int):
        holder: list[Node] = []
        self.holder[self.idx] = holder
        holder.extend((
            Node(holder, 0, left),
            Node(holder, 1, right),
        ))

    def __repr__(self):
        return f"Node({self.stone})"


def walk(holder: list):
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


def go(stones: list[int], total_blinks: int):
    root_holder: list[Node] = []
    root_holder.extend(Node(root_holder, idx, stone) for idx, stone in enumerate(stones))

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

    return len(list(walk(root_holder)))
