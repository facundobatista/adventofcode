import collections
import operator
from functools import reduce

# lines = """
# Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
# Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
# Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
# Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
# Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
# """
# lines = lines.strip().split("\n")

lines = open("input", "rt").readlines()

LIMITS = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

total = 0
counter = collections.Counter()
for line in lines:
    print("==== line", repr(line))
    header, data = line.split(":")
    game_id = int(header.split()[1].strip())

    fewest = {}
    gamesets = data.split(";")
    for gs in gamesets:
        all_retrieved = gs.split(",")
        for retrieved in all_retrieved:
            retrieved = retrieved.strip()
            quant, color = retrieved.split()
            quant = int(quant)
            fewest[color] = max(fewest.get(color, 0), quant)
    print("====== f", fewest)
    total += reduce(operator.mul, fewest.values())

print("Total", total)
