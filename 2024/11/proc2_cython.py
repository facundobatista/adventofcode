import sys

import proc2_cython_mod

lines_str = """
0 1 10 99 999
"""
total_blinks = 75
total_blinks = 30

# lines = """
#     125 17
# """
# total_blinks = 6
# total_blinks = 25

if sys.argv[1] == "test":
    lines = lines_str.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()


assert len(lines) == 1
stones = [int(x) for x in lines[0].split()]
total = proc2_cython_mod.go(stones, total_blinks)
print("Total:", total)
