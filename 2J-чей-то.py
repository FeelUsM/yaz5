from sys import stdin
input = stdin.readline


def debug(*args):
    if False:
        print(*args)


def solve():
    rows, cols = map(int, input().split())
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    letter = "a"
    grid = []
    for _ in range(rows):
        line = list(input().strip())
        grid.append(line)

    for row, line in enumerate(grid):
        for col, val in enumerate(line):
            if val == "#":
                if letter == "c":
                    debug("D")
                    return None

                top = left = float('inf')
                bottom = right = float('-inf')
                cnt = 1
                stack = [(row, col)]
                grid[row][col] = letter
                while stack:
                    x, y = stack.pop()
                    left = min(left, y)
                    right = max(right, y)
                    top = min(top, x)
                    bottom = max(bottom, x)

                    debug("Z", (x, y), top, left, bottom, right)
                    for move in moves:
                        dx = x + move[0]
                        dy = y + move[1]
                        if 0 <= dx < rows and 0 <= dy < cols and grid[dx][dy] == "#":
                            grid[dx][dy] = letter
                            stack.append((dx, dy))
                            cnt += 1

                width = right - left + 1
                height = bottom - top + 1
                if cnt != width * height:
                    if letter == "b":
                        debug("C1")
                        return None

                    prev_set = set()
                    b_set = set()
                    sizes = []

                    for subrow in range(top, bottom + 1):
                        size = 0
                        start_pos = right
                        curr_set = set()
                        inside = False
                        outside = False
                        for subcol in range(left, right + 1):
                            if grid[subrow][subcol] == ".":
                                if inside:
                                    outside = True
                                else:
                                    continue
                            elif outside:
                                return None
                            if not outside:
                                if not inside:
                                    start_pos = subcol
                                inside = True
                                debug("Q", (subrow, subcol), grid[subrow][subcol])
                                curr_set.add((subrow, subcol))
                                size += 1

                        if not sizes or sizes[-1] != (size, start_pos):
                            if len(sizes) == 1:
                                prev_set = curr_set
                            sizes.append((size, start_pos))
                        else:
                            prev_set.update(curr_set)

                    debug(curr_set, sizes)
                    debug("XXX", top, left, bottom, right)
                    if len(sizes) != 2:
                        debug("C2")
                        prev_set = set()
                        b_set = set()
                        sizes = []

                        for subcol in range(left, right + 1):
                            curr_set = set()
                            size = 0
                            start_pos = right
                            inside = False
                            outside = False
                            for subrow in range(top, bottom + 1):
                                if grid[subrow][subcol] == ".":
                                    if inside:
                                        outside = True
                                    else:
                                        continue
                                elif outside:
                                    return None
                                if not outside:
                                    if not inside:
                                        start_pos = subrow
                                    inside = True
                                    debug("Q", (subrow, subcol), grid[subrow][subcol])
                                    curr_set.add((subrow, subcol))
                                    size += 1

                            if not sizes or sizes[-1] != (size, start_pos):
                                if len(sizes) == 1:
                                    prev_set = curr_set
                                sizes.append((size, start_pos))
                            else:
                                prev_set.update(curr_set)

                        if len(sizes) != 2:
                            return None

                    for subrow, subcol in prev_set:
                        grid[subrow][subcol] = "b"

                    letter = "c"
                    debug(cnt, width, height)
                if letter == "a":
                    letter = "b"
                else:
                    letter = "c"

                debug("z", top, left, bottom, right)


    if letter == "a":
        debug("A")
        return None

    if letter == "b":
        if height * width == 1:
            debug("B")
            return None

        if height == 1 or width == 1:
            debug("X", top, left, bottom, right)
            grid[top][left] = "b"
        else:
            for col in range(left, right + 1):
                grid[top][col] = "b"
            debug("Y")

    return grid


#for _ in range(int(input())):
res = solve()
if res is None:
    print("NO")
else:
    print("YES")
    for line in res:
        print("".join(line))
