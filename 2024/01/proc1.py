import sys

lines = """
3   4
4   3
2   5
1   3
3   9
3   3
"""

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()


# load everything
seq1, seq2 = zip(*(line.strip().split() for line in lines))
seq1 = sorted(map(int, seq1))
seq2 = sorted(map(int, seq2))
diffs = (abs(x - y) for x, y in zip(seq1, seq2))
print("Total:", sum(diffs))
