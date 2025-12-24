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
file_meta = {}
try:
    while True:
        # file
        q_pos = next(imap)
        file_meta[file_id] = (disk_ptr, q_pos)
        for _ in range(q_pos):
            expanded[disk_ptr] = file_id
            disk_ptr += 1
        file_id += 1

        # space
        q_pos = next(imap)
        disk_ptr += q_pos

except StopIteration:
    # done
    pass

print("============== expanded", expanded)


def find_hole(file_id):
    # find a suitable hole
    hole_len = None
    initial_idx = None
    for idx, value in enumerate(expanded):
        # print("===== walk", idx, value)
        if value == file_id:
            # reached the file that trying to move, so no hole
            return

        if hole_len is None:
            # hole still not detected
            if value is None:
                # first item of a hole!
                hole_len = 1
                initial_idx = idx
        else:
            # walking a hole
            if value is None:
                hole_len += 1
            else:
                # hole interrupted
                hole_len = None
                initial_idx = None

        if hole_len is not None and hole_len == fsize:
            # useful hole!!!
            print("========== useful!", hole_len, initial_idx)
            return initial_idx

    # walked all disk, no good hole found
    print("============ nothing found")


# move from last file_id to 0 (file id is substracted because it was incremented one more
# than used when expanding)
for file_id in range(file_id - 1, -1, -1):
    finit, fsize = file_meta[file_id]
    print("======= file?", file_id, fsize)

    # get hole initial position
    initial_idx = find_hole(file_id)
    if initial_idx is None:
        continue

    # move the file to new position
    expanded[initial_idx:initial_idx + fsize] = [file_id] * fsize
    expanded[finit:finit + fsize] = [None] * fsize
    # print("============== expanded", expanded)


checksum = sum(idx * value for idx, value in enumerate(expanded) if value is not None)
print("Checksum:", checksum)
