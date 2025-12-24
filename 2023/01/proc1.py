values = []

with open("input", "rt") as fh:
    for line in fh:
        first_digit = None
        last_digit = None
        for char in line:
            if char.isdigit() and first_digit is None:
                first_digit = char
            if char.isdigit():
                last_digit = char
        values.append(int(first_digit + last_digit))
print(sum(values))
