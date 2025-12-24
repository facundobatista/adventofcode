import re

# lines = """
# 467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..
# """
# lines = lines.strip().split("\n")

lines = [x.strip() for x in open("input", "rt")]

LIMITS = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

matrix = [list(line) for line in lines]

total = 0
for idx, line in enumerate(lines):
    print("======= L", repr(line))
    matches = re.finditer(r"(\d+)", line)
    for rematch in matches:
        number = rematch.group()
        inipos, endpos = rematch.span()
        print("======== n", number)
        around = []

        # around current line
        if inipos > 0:
            around.append(matrix[idx][inipos - 1])
        try:
            around.append(matrix[idx][endpos])
        except IndexError:
            pass
        print("======= AR 0", around)

        # previous line
        if idx > 0:
            prev_line = matrix[idx - 1]
            prpos = inipos - 1 if inipos > 0 else inipos
            around.extend(prev_line[prpos: endpos + 1])
        print("======= AR 1", around)

        # next line
        if idx < len(matrix) - 1:
            next_line = matrix[idx + 1]
            prpos = inipos - 1 if inipos > 0 else inipos
            around.extend(next_line[prpos: endpos + 1])
        print("======= AR 2", around)

        around = [x for x in set(around) if x != "." and not x.isdigit()]
        print("======= AR F", around)
        if around:
            total += int(number)

print("Total", total)
