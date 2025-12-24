with open("input") as fh:
    c = 0
    prv = None
    for line in fh:
        line = line.strip()
        if not line:
            continue
        value = int(line)
        if prv is None:
            prv = value
            continue

        if value > prv:
            c += 1
        prv = value
print(c)
