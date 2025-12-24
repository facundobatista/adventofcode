import functools
import sys

lines = """
029A
980A
179A
456A
379A
"""
should_result = 126384
robot_layers = 2
should_result = 29483712
robot_layers = 8
should_result = 1157680330
robot_layers = 12


if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
    should_result = None
    robot_layers = 25
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

BOARDS = {
    "numspad": numspad,
    "ctrlpad": ctrlpad,
}


@functools.cache
def get_seqs(src_x, src_y, dst_x, dst_y, hole_coords):
    # print("================= get seq, ini", src_x, src_y, dst_x, dst_y)
    diff_x = dst_x - src_x
    diff_y = dst_y - src_y
    char_x, delta_x = (">", 1) if diff_x > 0 else ("<", -1)
    char_y, delta_y = ("v", 1) if diff_y > 0 else ("^", -1)

    # print("================= get seq, movs", (char_x, diff_x, char_y, diff_y))
    if diff_x == 0:
        all_seqs = [
            [char_y] * abs(diff_y),
        ]
    elif diff_y == 0:
        all_seqs = [
            [char_x] * abs(diff_x),
        ]
    else:
        all_seqs = [
            [char_x] * abs(diff_x) + [char_y] * abs(diff_y),
            [char_y] * abs(diff_y) + [char_x] * abs(diff_x),
        ]
    # print("================= get seq, seqs all", len(all_seqs))

    # avoid hole in the keyboard
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
            return tuple(seq) + ("A",)
    raise ValueError()


@functools.cache
def intermediate(board_name, topress):
    print("========= interm ?", board_name, topress)
    board = BOARDS[board_name]
    hole_coords = board["X"]
    cur_x, cur_y = board["A"]  # always starts in the A
    allseqs = []
    for key in topress:
        nxt_x, nxt_y = board[key]
        # print("========= nxt", key)
        seqs = get_seqs(cur_x, cur_y, nxt_x, nxt_y, hole_coords)
        allseqs.append(seqs)
        cur_x, cur_y = nxt_x, nxt_y

    print("========= interm seqs", allseqs)
    return tuple(allseqs)


sum_seq_cache = {}


def keyin(topress, count):
    print("====== keying ?", topress, count)
    # if count > 10:
    #     print("======= keyin", count)
    for seq in topress:
        subseqs = intermediate("ctrlpad", seq)
        if count:
            yield from keyin(subseqs, count - 1)
        else:
            value = sum_seq_cache.get(subseqs)
            if value is None:
                print("========= SS", subseqs)
                value = sum(len(seq) for seq in subseqs)
                sum_seq_cache[subseqs] = value
            yield value


allpads = [numspad, ctrlpad, ctrlpad]
seqlens = []
for srcseq in lines:
    print("\n============= SRC seq", repr(srcseq))

    # first layer, the numeric pad
    produced_seq = intermediate("numspad", srcseq)
    print("================== PART 1", produced_seq)

    # # N layers, the used by the robots
    # for layer in range(2, robot_layers + 2):
    #     produced_seq = keyin(produced_seq)
    #     print(f"================== PART {layer} total", len(produced_seq))  # , produced_seq)

    # N layers, the used by the robots
    subtotal = 0
    for seq_len in keyin(produced_seq, robot_layers - 1):
        subtotal += seq_len
    print("========= subt !!", subtotal)

    seqlens.append(subtotal)

total = 0
for srcseq, lenseq in zip(lines, seqlens):
    seqnum = int(srcseq.lstrip("0").rstrip("A"))
    print("====== result", (lenseq, seqnum))
    total += seqnum * lenseq

print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
