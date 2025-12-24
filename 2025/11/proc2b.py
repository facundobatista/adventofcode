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


def _parse_lines(lines):
    devices = {}
    for line in lines:
        src, alldest = line.split(": ")
        devices[src] = alldest.split()
    return devices

_cache = {}

def track(graph, next_node, end):
    key = (next_node, end)
    if key in _cache:
        return _cache[key]

    if next_node == end:
        return 1
    if next_node not in graph:
        return 0

    counter = 0

    for node in graph[next_node]:
        value = track(graph, node, end)
        counter += value

    _cache[key] = counter
    return counter


def run(lines):
    devices = _parse_lines(lines)
    print("====== dev", devices)
    ini_to_fft = track(devices, "svr", "fft")
    print("===== init to fft", ini_to_fft)
    ini_to_dac = track(devices, "svr", "dac")
    print("===== init to dac", ini_to_dac)
    dac_to_fft = track(devices, "dac", "fft")
    print("===== dac to fft", dac_to_fft)
    fft_to_dac = track(devices, "fft", "dac")
    print("===== fft to dac", fft_to_dac)
    dac_to_out = track(devices, "dac", "out")
    print("===== dac to out", dac_to_out)
    fft_to_out = track(devices, "fft", "out")
    print("===== fft to out", fft_to_out)

    p1 = ini_to_fft * fft_to_dac * dac_to_out
    p2 = ini_to_dac * dac_to_fft * fft_to_out
    return p1 + p2
