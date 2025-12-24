import sys

lines = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()

# process input
rules = []
updates = []
lines = iter(lines)
for line in lines:
    line = line.strip()
    if not line:
        break
    rules.append([int(x) for x in line.split("|")])
for line in lines:
    line = line.strip()
    updates.append([int(x) for x in line.split(",")])
print("====== rules", len(rules))
print("====== updates", len(updates))


def complies(update):
    print("====== update", update)
    for page1, page2 in rules:
        try:
            pos1 = update.index(page1)
            pos2 = update.index(page2)
        except ValueError:
            # rule mention a page that does not exist, it does not apply
            continue
        print("====== pages", page1, pos1, page2, pos2)
        if pos1 > pos2:
            return False
    return True


total = 0
for update in updates:
    if complies(update):
        print("====== YES")
        assert len(update) % 2 == 1
        middle = update[len(update) // 2]
        print("====== middle", middle)
        total += middle
    else:
        print("====== nop")

print("Total:", total)
