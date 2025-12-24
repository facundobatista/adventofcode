test_lines = """
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""
expected_test_result = 5

START = "you"
END = "out"
counter = 0


def _parse_lines(lines):
    devices = {}
    for line in lines:
        src, alldest = line.split(": ")
        devices[src] = alldest.split()
    return devices


def track(graph, next_node):
    global counter

    for node in graph[next_node]:
        if node == END:
            counter += 1
        else:
            track(graph, node)


def run(lines):
    devices = _parse_lines(lines)
    print("====== dev", devices)
    track(devices, START)
    return counter
