depth = 0
pos_x = 0
aim = 0
with open("input") as fh:
    for line in fh:
        action, val = line.strip().split()
        val = int(val)
        if action == "forward":
            pos_x += val
            depth += aim * val
        elif action == "down":
            aim += val
        elif action == "up":
            aim -= val
        else:
            raise ValueError(f"Bad line: {line!r}")
print(depth * pos_x)
