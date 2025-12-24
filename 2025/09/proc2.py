import itertools

from safe_map import SafeMap


test_lines = """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""
expected_test_result = 24

RED = "#"
GREEN = "X"


def _parse_lines(lines):
    lines = [x.split(",") for x in lines]
    lines = [tuple(map(int, item)) for item in lines]
    return lines


def run(lines):
    lines = _parse_lines(lines)

    # normalize to 1 to avoid a crazy big map
    base = lines[0][0]
    for x, y in lines:
        base = min(base, x, y)
    print("========= base", base)
    delta = base - 1  # not to 0, to not have useful tiles glued to the left
    print("====== bef", lines[:3])
    lines = [(x - delta, y - delta) for x, y in lines]
    print("====== aft", lines[:3])

    # paint the walls between corner coordinates, and save for later what to paint
    # inside (from the wall cell, "to inside")
    coord_from = lines[0]
    path_points = []
    for coord_to in lines[1:] + [lines[0]]:  # add first again to close loop
        xf, yf = coord_from
        xt, yt = coord_to
        if (xf == xt and yf == yt) or (xf != xt and yf != yt):
            raise ValueError("bad source path")

        if xf == xt:
            if yf < yt:
                # vertical down
                for y in range(yf, yt):
                    path_points.append((xf, y))
            else:
                # vertical up
                for y in range(yf, yt, -1):
                    path_points.append((xf, y))
        else:
            if xf < xt:
                # horizontal right
                for x in range(xf, xt):
                    path_points.append((x, yf))
            else:
                # horizontal left
                for x in range(xf, xt, -1):
                    path_points.append((x, yf))

        coord_from = coord_to

    print("=========== path points", len(path_points))
    minx = maxx = lines[0][0]
    miny = maxy = lines[0][1]
    for x, y in lines[1:]:
        minx = min(minx, x)
        maxx = max(maxx, x)
        miny = min(miny, y)
        maxy = max(maxy, y)
    assert minx > 0 and miny > 0
    print("======== size", maxx, maxy)
    smap = SafeMap(size=(maxx + 1, maxy + 1))
    smap.draw_loop(path_points, GREEN, fill=GREEN)
    smap.show()

    maxarea = 0
    for c1, c2 in itertools.combinations(lines, 2):
        w = abs(c1[0] - c2[0]) + 1
        h = abs(c1[1] - c2[1]) + 1
        area = w * h

        if area > maxarea:
            # candidate! make it ok only if all is inside green area
            print("=============== check!", c1, c2)
            x1, y1 = c1
            x2, y2 = c2
            fx, tx = min(x1, x2), max(x1, x2) + 1
            fy, ty = min(y1, y2), max(y1, y2) + 1

            for x, y in itertools.product(range(fx, tx), range(fy, ty)):
                print("========== xy", x, y)
                if smap[(x, y)] != GREEN:
                    break
            else:
                # all green!!
                print("=========== VERDEEEEE", area)
                maxarea = area

    return maxarea
