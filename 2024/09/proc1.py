import sys

lines = """
2333133121414131402
"""

# lines = """
# 12345
# """

if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
else:
    print("Bad arg")
    exit()

assert len(lines) == 1
disk_map = [int(x) for x in lines[0].strip()]

disk_len = sum(disk_map)
print("Disk len:", disk_len)

# expand it
expanded = [None] * disk_len
imap = iter(disk_map)
file_id = 0
disk_ptr = 0
q_empty = 0
try:
    while True:
        # file
        q_pos = next(imap)
        for _ in range(q_pos):
            expanded[disk_ptr] = file_id
            disk_ptr += 1
        file_id += 1

        # space
        q_pos = next(imap)
        disk_ptr += q_pos
        q_empty += q_pos

except StopIteration:
    # done
    pass

print("============== expanded", expanded)

# defrag - the pointer will go from start to the eventual end of defragmented disk, which is
# the total length minus the quantity of empty blocks (which are all in the end, because defrag)
defrag_len = disk_len - q_empty
for ptr in range(defrag_len):
    print("======= to ptr", ptr, expanded[ptr])
    if expanded[ptr] is None:
        while True:
            last = expanded.pop()
            print("=======   moving", last)
            if last is not None:
                expanded[ptr] = last
                break
print("============== expanded", expanded)

checksum = sum(idx * value for idx, value in enumerate(expanded[:defrag_len]))
print("Checksum:", checksum)
