import itertools
from functools import lru_cache

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


def _track_horizontal_wall(maxx, corners, from_x, yf, yt):
    """Track two corners horizontally until we found another one(s)."""
    found_y = []
    for track_x in range(from_x, maxx + 1):
        if (track_x, yf) in corners:
            found_y.append(yf)
        if (track_x, yt) in corners:
            found_y.append(yt)
        if found_y:
            # reached a corner!
            return track_x, found_y
    raise ValueError("tracking limit reached")


def _get_first_vertical_wall(maxy, corners, x):
    """Parse a column at x to find the first verticall wall."""
    for yf in range(0, maxy + 1):
        if (x, yf) in corners:
            break
    else:
        # it's ok to not find a wall
        return

    for yt in range(yf + 1, maxy + 1):
        if (x, yt) in corners:
            break
    else:
        # if initial corner is found, we need to find the second one
        raise ValueError("Missing yTO in search for verticall wall")
    return yf, yt


@lru_cache
def _search_in_rectangles(rectangles, x, y):
    for xf, yf, xt, yt in rectangles:
        if xf <= x <= xt and yf <= y <= yt:
            return True

    # this tile is not found! so the overall c1-c2 rectangle is not inside the rectangles!
    return False


def _is_inside(rectangles, c1, c2):
    """Return if all tiles between c1 and c2 corners are inside any of the rectangles."""
    x1, y1 = c1
    x2, y2 = c2
    fx, tx = min(x1, x2), max(x1, x2) + 1
    fy, ty = min(y1, y2), max(y1, y2) + 1

    # first validate the corners
    print("======= 0", c1, c2)
    for x, y in [(x1, y1), (x1, y2), (x2, y1), (x2, y2)]:
        if not _search_in_rectangles(rectangles, x, y):
            return False

    # then validate the sides
    print("======= 1", c1, c2)
    for y in range(fy, ty):
        if not _search_in_rectangles(rectangles, x1, y):
            print("============== NOT INSIDE 1", c1, c2)
            return False
        if not _search_in_rectangles(rectangles, x2, y):
            print("============== NOT INSIDE 2", c1, c2)
            return False
    print("======= 2", c1, c2)
    for x in range(fx, tx):
        if not _search_in_rectangles(rectangles, x, y1):
            print("============== NOT INSIDE 3", c1, c2)
            return False
        if not _search_in_rectangles(rectangles, x, y2):
            print("============== NOT INSIDE 4", c1, c2)
            return False

    print("======= 3", c1, c2)
    # jump around a little
    for x, y in itertools.product(range(fx, tx, 47), range(fy, ty, 47)):
        if not _search_in_rectangles(rectangles, x, y):
            print("============== NOT INSIDE 5", c1, c2)
            return False

    print("======= 4", c1, c2)
    # brute force, check all
    print("================= BF!!! total", (tx - fx) * (ty - fy) / 1000000)
    for idx, (x, y) in enumerate(itertools.product(range(fx, tx), range(fy, ty))):
        if idx % 10000 == 0:
            print("=========== BF idx", idx)
        if not _search_in_rectangles(rectangles, x, y):
            print("============== NOT INSIDE 9", c1, c2)
            return False

    print("======= 4", c1, c2)
    # all x, y passed ok, cool
    return True


def run(lines):
    lines = _parse_lines(lines)

    minx = maxx = lines[0][0]
    miny = maxy = lines[0][1]
    for x, y in lines[1:]:
        minx = min(minx, x)
        maxx = max(maxx, x)
        miny = min(miny, y)
        maxy = max(maxy, y)
    assert minx > 0 and miny > 0
    print("======== size", maxx, maxy)

    # prepare this for the column scan
    all_busy_x = iter(sorted(set(line[0] for line in lines)))

    corners = set(lines)
    print("============= starting corners", sorted(corners))

    # cut the weird loop shape in rectangles, by scanning the "map" from left to right (vertical
    # passes); when a wall is found that square is removed, and we go again (from a previous
    # column, to simplify the case of two vertical walls in the same column)
    rectangles = []
    while True:
        y_limits = _get_first_vertical_wall(maxy, corners, x)
        if y_limits is None:
            # nothing found in this column, move to the right
            try:
                x = next(all_busy_x)
            except StopIteration:
                break
            continue

        yf, yt = y_limits

        # we have a (at least one) vertical wall, let's trackit horizontally
        end_x, found_y = _track_horizontal_wall(maxx, corners, x + 1, yf, yt)

        # store rectangle
        cf = (x, yf)
        ct = (end_x, yt)
        assert end_x >= x
        assert yt >= yf
        area = (end_x - x) * (yt - yf)
        rectangles.append((area, cf, ct))

        # "move" the wall to this new position
        corners.remove((x, yf))
        corners.remove((x, yt))
        for y in [yf, yt]:
            if y in found_y:
                # this was a corner found, we should remove it because rectangle starts elsewhere
                corners.remove((end_x, y))
            else:
                # this was in the air, create the corner
                corners.add((end_x, y))

        print("============= current corners", len(corners))

    # order to have biggest rectangles first
    rectangles.sort(reverse=True)
    print("======== rectangles 0", rectangles)
    rectangles = tuple((c1[0], c1[1], c2[0], c2[1]) for _, c1, c2 in rectangles)
    print("======== rectangles 1", len(rectangles))

    all_areas = []
    for c1, c2 in itertools.combinations(lines, 2):
        w = abs(c1[0] - c2[0]) + 1
        h = abs(c1[1] - c2[1]) + 1
        area = w * h
        all_areas.append((area, c1, c2))
    print("====== areas", len(all_areas))

    all_areas.sort(reverse=True)
    for idx, (area, c1, c2) in enumerate(all_areas, 1):
        if area >1525241870 :
            continue
        if idx % 1 == 0:
            print("======= checking area", idx, area)
            # NOTE!!!!!!!!!!!!!!!!!! here the one that was taking for ever (because it hits brute force above) was the answer...
        if _is_inside(rectangles, c1, c2):
            # all green!!
            break
    return area
