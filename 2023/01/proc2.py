# lines = """
# two1nine
# eightwothree
# abcone2threexyz
# xtwone3four
# 4nineeightseven2
# zoneight234
# 7pqrstsixteen
# # twohbkkrzvpxeighttczsls4six5nineeight
# """
# lines = lines.strip().split("\n")

lines = open("input", "rt").readlines()

numbers = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def npos2int(pos):
    number = npos[pos]
    return numbers[number]


total = 0
for line in lines:
    npos = {}
    for number in numbers:
        pos = -1
        while True:
            pos = line.find(number, pos + 1)
            if pos == -1:
                break
            npos[pos] = number
    print("=== nps", npos)
    value = npos2int(min(npos)) * 10 + npos2int(max(npos))
    print("=======", repr(line), value)
    total += value
print("Total", total)
