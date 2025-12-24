values = []
with open("input") as fh:
    for line in fh:
        line = line.strip()
        if not line:
            continue
        value = int(line)
        values.append(value)

slides = [None] * len(values)
for idx, value in enumerate(values):
    slides[idx] = value
    if idx >= 1:
        slides[idx - 1] += value
    if idx >= 2:
        slides[idx - 2] += value

# last two don't have 3 values
slides = slides[:-2]

c = 0
prv = None
for value in slides:
    if prv is None:
        prv = value
        continue

    if value > prv:
        c += 1
    prv = value
print(c)
