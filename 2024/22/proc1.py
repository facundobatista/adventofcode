import sys

lines = """
1
10
100
2024
"""
should_result = 37327623

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
    should_result = None
else:
    print("Bad arg")
    exit()

inits = [int(x.strip()) for x in lines]


def get_nth(secnum, iterations):
    for idx in range(1, iterations + 1):
        # Calculate the result of multiplying the secret number by 64. Then, mix this result
        # into the secret number. Finally, prune the secret number.
        result = secnum * 64
        secnum = result ^ secnum  # mix
        secnum = secnum % 16777216

        # Calculate the result of dividing the secret number by 32. Round the result down to the
        # nearest integer. Then, mix this result into the secret number. Finally, prune the secret
        # number.
        result = secnum // 32
        secnum = result ^ secnum  # mix
        secnum = secnum % 16777216

        # Calculate the result of multiplying the secret number by 2048. Then, mix this result into
        # the secret number. Finally, prune the secret number.
        result = secnum * 2048
        secnum = result ^ secnum  # mix
        secnum = secnum % 16777216

        # print("======== nth", idx, secnum)

    return secnum


total = 0
for init in inits:
    sn = get_nth(init, 2000)
    print("==== init", init, sn)
    total += sn

print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
