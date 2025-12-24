import sys
from collections import deque

lines = """
1
2
3
2024
"""
should_result = 23

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
    should_result = None
else:
    print("Bad arg")
    exit()

inits = [int(x.strip()) for x in lines]


def get_nth(secnum, iterations):
    diffs = []
    prv = secnum % 10
    for idx in range(1, iterations + 1):
        # Calculate the result of multiplying the secret number by 64. Then, mix this result
        # into the secret number. Finally, prune the secret number.
        result = secnum * 64
        secnum = result ^ secnum  # mix
        secnum = secnum % 16777216

        # Calculate the result of dividing the secret number by 32. Round the result down to the
        # nearest integer. Then, mix this result into the secret number. Finally, prune the secret
        # number.
        result = secnum // 32
        secnum = result ^ secnum  # mix
        secnum = secnum % 16777216

        # Calculate the result of multiplying the secret number by 2048. Then, mix this result into
        # the secret number. Finally, prune the secret number.
        result = secnum * 2048
        secnum = result ^ secnum  # mix
        secnum = secnum % 16777216

        lastdig = secnum % 10
        diff = lastdig - prv
        # print("========= get nth", idx, lastdig, diff)
        diffs.append((lastdig, diff))
        prv = lastdig

    return diffs



buyerseqs = []
allseqs = set()
for init in inits:
    pricesdiffs = get_nth(init, 2000)
    # print("======= xxx", pricesdiffs)
    seqs = {}
    diff4 = deque(maxlen=4)
    diff4.extend(diff for _, diff in pricesdiffs[:3])
    for idx, (price, diff) in enumerate(pricesdiffs[3:]):
        diff4.append(diff)
        t4 = tuple(diff4)
        # print("======s", idx, t4, price)
        seqs.setdefault(t4, price)
        allseqs.add(t4)
    buyerseqs.append(seqs)

print("======= all seqs?", len(allseqs))
max_bananas = 0
for seq in allseqs:
    local = sum(bs.get(seq, 0) for bs in buyerseqs)
    # print("=== seq", seq, local)
    max_bananas = max(max_bananas, local)
    if max_bananas == local:
        print("============= AMX", local, seq)
total = max_bananas

print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
