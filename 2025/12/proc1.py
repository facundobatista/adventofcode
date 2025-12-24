from safe_map import SafeMap

test_lines = """
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""
expected_test_result = 2

MARK_ROLL = "@"
MARK_EMPTY = "."


def _flip_v(shape):
    """Split vertically. Note first dimension is Y (classic list of lists)."""
    shape = [shape[2], shape[1], shape[0]]
    return shape


def _flip_h(shape):
    """Split horizontally. Note first dimension is Y (classic list of lists)."""
    shape = [
        [shape[0][2], shape[0][1], shape[0][0]],
        [shape[1][2], shape[1][1], shape[1][0]],
        [shape[2][2], shape[2][1], shape[2][0]],
    ]
    return shape


def _rotate(shape):
    """Rotate 90° clockwise. Note first dimension is Y (classic list of lists)."""
    shape = [
        [shape[2][0], shape[1][0], shape[0][0]],
        [shape[2][1], shape[1][1], shape[0][1]],
        [shape[2][2], shape[1][2], shape[0][2]],
    ]
    return shape


def _explode_alternatives(shape):
    """Return all the alternatives (rotated, flipped) for a shape.

    We get them all by flipping vertically and horizontally, rotating 90°, and flipping both again.
    """
    alternatives = [shape]
    assert len(shape) == len(shape[0]) == 3  # code very specific for a 3x3 grid

    alternatives.append(_flip_v(shape))
    alternatives.append(_flip_h(shape))

    shape = _rotate(shape)
    alternatives.append(shape)

    alternatives.append(_flip_v(shape))
    alternatives.append(_flip_h(shape))

    return alternatives


def parse(lines):
    lines = iter(lines)

    raw_shapes = []
    while True:
        sid = next(lines)
        if sid[-1] != ":":
            break
        sid = int(sid[:-1])
        assert len(raw_shapes) == sid
        raw_shapes.append([next(lines) for _ in range(3)])
        assert next(lines) == ""
    print("======== raw shapes", raw_shapes)

    raw_regions = [sid]
    raw_regions.extend(lines)
    print("========== raw regions", raw_regions)

    # process shapes
    shapes = []
    for raw in raw_shapes:
        shape = [list(row) for row in raw]
        shapes.append(_explode_alternatives(shape))
    print("======== shapes", shapes)

    deltas = set()
    shapes_deltas = {}
    for idx, comb in enumerate(shapes):
        print("\n======================shshshs", idx)
        for shape in comb:
            SafeMap(shape).show()
            delta = []
            for y, row in enumerate(shape):
                for x, cell in enumerate(row):
                    if cell == "#":
                        delta.append((x, y))
            print("\n======================delta", delta)
            deltas.add(tuple(delta))
        shapes_deltas[idx] = deltas

    # process regions
    regions = []
    for raw in raw_regions:
        raw_size, raw_presents = raw.split(": ")
        sh, sv = raw_size.split("x")
        region = ((int(sh), int(sv)), list(map(int, raw_presents.split())))
        regions.append(region)
    print("========== regions", regions)

    return shapes_deltas, regions


def run(lines):
    deltas, regions = parse(lines)
    print("======== full deltas", deltas)
    occupied = {}
    for did, combinations in deltas.items():
        print("======= com", combinations)
        occupied[did] = len(list(combinations)[0])

    print("======= FILTR totales", len(regions))
    regions2 = []
    for (w, h), to_fit in regions:
        size = w * h
        slots = sum(occupied[did] * quant for did, quant in enumerate(to_fit))
        if slots <= size:
            regions2.append((size, to_fit))

    print("======= FILTR basico", len(regions2))
    justplaced = 0
    regions3 = []
    for size, to_fit in regions2:
        slots = sum(9 * quant for quant in to_fit)
        if slots <= size:
            justplaced += 1
        else:
            regions3.append((size, to_fit))

    print("======= FILTR just placed", justplaced)
    print("======= FILTR nos queda", len(regions3))
