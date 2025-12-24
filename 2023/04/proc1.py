import sys

lines = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()


total = 0
for line in lines:
    print("======= L", repr(line))
    title, data = line.split(":")
    winning, owned = data.split("|")
    winning = set(x.strip() for x in winning.split())
    winning.discard("")
    owned = set(x.strip() for x in owned.split())
    owned.discard("")
    scored = winning & owned
    print("========sc", scored)
    if scored:
        total += 2 ** (len(scored) - 1)

print("Total", total)
