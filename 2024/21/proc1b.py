import functools
import itertools
import sys

lines = """
029A
980A
179A
456A
379A
"""
should_result = 126384


if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
    should_result = None
else:
    print("Bad arg")
    exit()


# the numeric keyboard
# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+
numspad = {
    "X": (0, 3),
    "0": (1, 3),
    "A": (2, 3),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
}

# the control pad
#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
ctrlpad = {
    "X": (0, 0),
    "^": (1, 0),
    "A": (2, 0),
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1),
}

# the delta that each button implies
button_delta = {
    ">": (1, 0),
    "<": (-1, 0),
    "^": (0, -1),
    "v": (0, 1),
}


@functools.cache
def get_seqs(src_x, src_y, dst_x, dst_y, hole_coords):
    print("================= get seq, ini", src_x, src_y, dst_x, dst_y)
    diff_x = dst_x - src_x
    diff_y = dst_y - src_y
    char_x, delta_x = (">", 1) if diff_x > 0 else ("<", -1)
    char_y, delta_y = ("v", 1) if diff_y > 0 else ("^", -1)

    movs = [char_x] * abs(diff_x) + [char_y] * abs(diff_y)
    print("================= get seq, movs", len(movs), movs)
    all_seqs = set(itertools.permutations(movs, len(movs)))
    print("================= get seq, seqs all", len(all_seqs))

    # avoid hole in the keyboard
    safe_seqs = []
    for seq in all_seqs:
        cur_x, cur_y = src_x, src_y
        for button in seq:
            dx, dy = button_delta[button]
            cur_x, cur_y = cur_x + dx, cur_y + dy
            if (cur_x, cur_y) == hole_coords:
                break
        else:
            # got to the end without hitting the hole
            assert cur_x == dst_x and cur_y == dst_y
            safe_seqs.append(list(seq))
    print("================= get seq, seqs saf", len(safe_seqs))

    # sizes, right?
    sample = len(safe_seqs[0])
    assert all(len(seq) == sample for seq in safe_seqs)

    # hit "A" button at the destination
    for seq in safe_seqs:
        seq.append("A")

    return safe_seqs


def keyin(board, topress):
    print("====== keying", topress, board)
    hole_coords = board["X"]
    cur_x, cur_y = board["A"]  # always starts in the A
    allseqs = []
    for key in topress:
        nxt_x, nxt_y = board[key]
        # print("========= nxt", key)
        seqs = get_seqs(cur_x, cur_y, nxt_x, nxt_y, hole_coords)
        allseqs.append(seqs)
        cur_x, cur_y = nxt_x, nxt_y
    # print("========= partial seqs", allseqs)

    combinseqs = []
    for combin in itertools.product(*allseqs):
        fullseq = []
        for seq in combin:
            fullseq.extend(seq)
        combinseqs.append(tuple(fullseq))
    # print("========= combind seqs", combinseqs)

    # sizes, right?
    sample = len(combinseqs[0])
    assert all(len(seq) == sample for seq in combinseqs)

    return combinseqs


allpads = [numspad, ctrlpad, ctrlpad]
seqlens = []
for srcseq in lines:
    print("\n============= SRC seq", repr(srcseq))

    # first layer
    produced_seqs = keyin(numspad, srcseq)
    print("================== PART 1", produced_seqs)

    # second layer
    next_seqs = set()
    for seq in produced_seqs:
        produced_seqs = keyin(ctrlpad, seq)
        print("================== PART 2", len(produced_seqs))
        next_seqs.update(produced_seqs)
    produced_seqs = next_seqs
    print("================== PART 2 total", len(produced_seqs))

    # third layer
    next_seqs = set()
    for seq in produced_seqs:
        produced_seqs = keyin(ctrlpad, seq)
        print("================== PART 3", len(produced_seqs))
        next_seqs.update(produced_seqs)
    produced_seqs = next_seqs
    print("================== PART 3 total", len(produced_seqs))

    # get the shortest
    sample = min(len(seq) for seq in produced_seqs)
    print("================== final, len", sample)
    seqlens.append(sample)

total = 0
for srcseq, lenseq in zip(lines, seqlens):
    seqnum = int(srcseq.lstrip("0").rstrip("A"))
    print("====== result", (lenseq, seqnum))
    total += seqnum * lenseq

print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
