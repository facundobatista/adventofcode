test_lines = """
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: eee ddd
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""
expected_test_result = 2

START = "svr"
END = "out"

SPECIALS = {
    "fft": 1,
    "dac": 2,
}


def _parse_lines(lines):
    devices = {}
    for line in lines:
        src, alldest = line.split(": ")
        devices[src] = alldest.split()
    return devices


_cache = {}


def track(graph, next_node, specs, deep):
    if next_node == END:
        return 1 if specs == 3 else 0  # visited both SPECIALS

    key = (next_node, specs, deep)
    counter = _cache.get(key)
    if counter is not None:
        print("======= cached!", next_node, specs, counter)
        return counter

    counter = 0

    print("======== next", next_node, specs)
    for node in graph[next_node]:
        specs += SPECIALS.get(node, 0)
        value = track(graph, node, specs, deep + 1)
        counter += value

    _cache[key] = counter
    print("======= calculted!", next_node, specs, counter)
    return counter


def run(lines):
    devices = _parse_lines(lines)
    print("====== dev", devices)
    counter = track(devices, START, 0, 0)
    return counter
