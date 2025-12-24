import sys
from heapq import heappop, heappush

lines = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""
should_result = 7036

# lines = """
# #################
# #...#...#...#..E#
# #.#.#.#.#.#.#.#.#
# #.#.#.#...#...#.#
# #.#.#.#.###.#.#.#
# #...#.#.#.....#.#
# #.#.#.#.#.#####.#
# #.#...#.#.#.....#
# #.#.#####.#.###.#
# #.#.#.......#...#
# #.#.###.#####.###
# #.#.#...#.....#.#
# #.#.#.#####.###.#
# #.#.#.........#.#
# #.#.#.#########.#
# #S#.............#
# #################
# """
# should_result = 11048


if sys.argv[1] == "test":
    lines = lines.strip().split("\n")
elif sys.argv[1] == "real":
    lines = [x.strip() for x in open("input", "rt")]
    should_result = None
else:
    print("Bad arg")
    exit()


def part1(grid):
    m, n = len(grid), len(grid[0])
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 'S':
                start = (i, j)
            elif grid[i][j] == 'E':
                end = (i, j)

    grid[end[0]] = grid[end[0]].replace('E', '.')

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    heap = [(0, 0, *start)]
    visited = set()
    while heap:
        score, d, i, j = heappop(heap)
        if (i, j) == end:
            break

        if (d, i, j) in visited:
            continue

        visited.add((d, i, j))

        x = i + directions[d][0]
        y = j + directions[d][1]
        if grid[x][y] == '.' and (d, x, y) not in visited:
            heappush(heap, (score + 1, d, x, y))

        left = (d - 1) % 4
        if (left, i, j) not in visited:
            heappush(heap, (score + 1000, left, i, j))

        right = (d + 1) % 4
        if (right, i, j) not in visited:
            heappush(heap, (score + 1000, right, i, j))

    return score

total = part1(lines)
print("Total:", total)
if should_result is not None:
    print("ok :)" if should_result == total else f"MAL! debería: {should_result!r}")
