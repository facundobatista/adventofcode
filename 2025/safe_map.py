class SafeMap:
    """A map that safely return out-of-map data."""

    EMPTY = "."

    # deltas
    DELTA_RIGHT = (1, 0)
    DELTA_LEFT = (-1, 0)
    DELTA_UP = (0, -1)
    DELTA_DOWN = (0, 1)
    RECT_DELTAS = [DELTA_UP, DELTA_RIGHT, DELTA_DOWN, DELTA_LEFT]
    DELTA_UP_RIGHT = (1, -1)
    DELTA_UP_LEFT = (-1, -1)
    DELTA_DOWN_RIGHT = (1, 1)
    DELTA_DOWN_LEFT = (-1, 1)
    ALL_DELTAS = [
        DELTA_UP,
        DELTA_UP_RIGHT,
        DELTA_RIGHT,
        DELTA_DOWN_RIGHT,
        DELTA_DOWN,
        DELTA_DOWN_LEFT,
        DELTA_LEFT,
        DELTA_UP_LEFT,
    ]
    _MARK = object()

    # XXX: we should split this into two classmethods; from_lines and from_size
    def __init__(self, lines=None, size=None, out_of_map=_MARK, empty=EMPTY):
        if (lines is None and size is None) or (lines is not None and size is not None):
            raise ValueError("Must indicate 'lines' XOR 'size'")
        if lines is not None:
            self.xmap = [list(line) for line in lines]
            self.max_x = len(self.xmap[0])
            self.max_y = len(self.xmap)
        if size is not None:
            w, h = size
            self.xmap = [[empty] * w for _ in range(h)]
            self.max_x = w
            self.max_y = h
        if out_of_map is self._MARK:
            def _f():
                raise ValueError("out of map")
            self.out_of_map = _f
        else:
            self.out_of_map = lambda: out_of_map
        self.empty = empty

    def __getitem__(self, coord):
        x, y = coord
        if (0 <= x < self.max_x) and (0 <= y < self.max_y):
            val = self.xmap[y][x]
        else:
            val = self.out_of_map()

        return val

    def __setitem__(self, coord, value):
        x, y = coord
        if (0 <= x < self.max_x) and (0 <= y < self.max_y):
            self.xmap[y][x] = value
        else:
            raise ValueError("out of map")

    def walk(self):
        """Walk through all the map."""
        for y in range(self.max_y):
            for x in range(self.max_x):
                val = self.xmap[y][x]
                yield x, y, val

    def switch(self, coord, delta):
        """Switch the element from the coordinate with the coordinate + delta."""
        x1, y1 = coord
        dx, dy = delta
        x2 = x1 + dx
        y2 = y1 + dy
        self.xmap[y1][x1], self.xmap[y2][x2] = self.xmap[y2][x2], self.xmap[y1][x1]
        return (x2, y2)

    def __str__(self):
        lines = []
        width = len(self.xmap[0])
        lines.append("-" * width)
        for row in self.xmap:
            lines.append("".join(item for item in row))
        lines.append("-" * width)
        return "\n".join(lines)

    def show(self):
        """Show the map."""
        print(self)

    def find(self, to_find):
        """Return the first ocurrence of item."""
        for y, row in enumerate(self.xmap):
            for x, item in enumerate(row):
                if item == to_find:
                    return x, y
        raise ValueError("Couldn't find " + repr(to_find))

    def _cross_simple_loop_wall(self):
        """Cross a simple loop's wall to find where is "inside", horizontally."""
        for y in range(self.max_y):
            if self[(0, y)] != self.empty:
                continue
            print("===== check hztal", y)
            for x in range(self.max_x):
                if self[(x, y)] != self.empty:
                    print("===========somethin detected", x)
                    # found something! if next char is empty, we're through a wall
                    if self[(x + 1, y)] == self.empty:
                        return (x + 1, y)
                    break

    def _spread(self, coord, fill):
        """Spread that fill char on all empty places starting from given coord."""
        print("======= spreadfilling", coord)
        self[coord] = fill
        for delta in self.RECT_DELTAS:
            nc = (coord[0] + delta[0], coord[1] + delta[1])
            if self[nc] == self.empty:
                self._spread(nc, fill)

    def draw_loop(self, path_points, border_char, fill=None):
        """Draw a loop in the map following the given path points/coords.

        If fill is not None, the loop will be filled with that char.
        """
        # draw it
        for x, y in path_points:
            print("=======d", x, y)
            self[(x, y)] = border_char

        if fill is None:
            return

        # find inside coord
        coord = self._cross_simple_loop_wall()
        if coord is None:
            raise NotImplementedError("missing to search wall vertically")

        # spread like dropping paint from that coord
        self._spread(coord, fill)
