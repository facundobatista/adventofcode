import functools
import sys
from collections import Counter

lines = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()


def _get_type(hand):
    print("===== hand", hand)
    cnt = Counter(hand)
    print("      cntr", cnt)
    if len(cnt) == 1:
        assert list(cnt.values()) == [5]
        result = 7  # five of a kind
    elif len(cnt) == 2:
        # 4 & 1, or 3 & 2
        if max(cnt.values()) == 4:
            result = 6  # four of a kind
        else:
            result = 5  # full house
    elif len(cnt) == 3:
        # 3 & 1 & 1, or 2 & 2 & 1
        if max(cnt.values()) == 3:
            result = 4  # three of a kind
        else:
            result = 3  # two pair
    elif len(cnt) == 4:
        # 2 & 1 & 1 & 1
        result = 2  # one pair
    else:
        assert len(cnt) == 5
        result = 1  # high card
    print("      rslt", result)
    return result


CARD_ORDER = list(reversed("AKQJT98765432"))


def handorder(full1, full2):
    hand1 = full1[0]
    hand2 = full2[0]
    print("==== order?", hand1, hand2)
    t1 = _get_type(hand1)
    t2 = _get_type(hand2)
    print("     types", t1, t2)

    if t1 < t2:
        result = -1
    elif t1 > t2:
        result = 1
    else:
        result = 0
        for c1, c2 in zip(hand1, hand2):
            i1 = CARD_ORDER.index(c1)
            i2 = CARD_ORDER.index(c2)
            if i1 < i2:
                result = -1
                break
            if i1 > i2:
                result = 1
                break

    print("     reslt", result)
    return result


# load everything
allgame = []
for line in lines:
    hand, bid = line.split()
    assert len(hand) == 5
    allgame.append((hand, int(bid)))
assert len(set(x[0] for x in allgame)) == len(allgame)

allgame.sort(key=functools.cmp_to_key(handorder))

total = 0
for rank, (hand, bid) in enumerate(allgame, 1):
    print("===== calc", rank, hand, bid)
    total += rank * bid

print("Total", total)
