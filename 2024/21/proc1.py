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
    "A": (2, 3),
    "0": (1, 3),
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
    "^": (1, 0),
    "A": (2, 0),
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1),
}


def get_seq(cur_x, cur_y, nxt_x, nxt_y):
    print("================= seq??", cur_x, cur_y, nxt_x, nxt_y)
    diff_x = nxt_x - cur_x
    diff_y = nxt_y - cur_y
    char_x = ">" if diff_x > 0 else "<"
    char_y = "v" if diff_y > 0 else "^"
    seq = [char_x] * abs(diff_x) + [char_y] * abs(diff_y)
    print("================= seq!!", seq)
    return seq


def get_seq(cur_x, cur_y, nxt_x, nxt_y):
    print("================= seq??", cur_x, cur_y, nxt_x, nxt_y)
    diff_x = nxt_x - cur_x
    diff_y = nxt_y - cur_y
    char_x = ">" if diff_x > 0 else "<"
    char_y = "v" if diff_y > 0 else "^"
    seq = [char_x] * abs(diff_x) + [char_y] * abs(diff_y)
    print("================= seq!!", seq)
    return seq


def keyin(board, topress):
    print("====== keying", topress, board)
    cur_x, cur_y = board["A"]  # always starts in the A
    allseq = []
    for key in topress:
        nxt_x, nxt_y = board[key]
        print("========= nxt", key)
        seq = get_seq(cur_x, cur_y, nxt_x, nxt_y)
        allseq.extend(seq)
        allseq.append("A")  # ENTER
        cur_x, cur_y = nxt_x, nxt_y
    return allseq


allpads = [numspad, ctrlpad, ctrlpad]
seqlens = []
for srcseq in lines:
    print("\n============= SRC seq", repr(srcseq))
    for idx, pad in enumerate(allpads):
        resseq = keyin(pad, srcseq)
        print("================== PART", idx, srcseq, resseq)
        srcseq = resseq
    print("================ final", len(srcseq), srcseq)
    seqlens.append(len(srcseq))

total = 0
for srcseq, lenseq in zip(lines, seqlens):
    seqnum = int(srcseq.lstrip("0").rstrip("A"))
    print("====== result", (srcseq, seqnum, lenseq))
    total += seqnum * lenseq

print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
