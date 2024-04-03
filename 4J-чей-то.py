from sys import stdin
input = stdin.readline



def get_shoelace_area(points):
    n = len(points)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += points[i][0] * points[j][1] - points[j][0] * points[i][1]
    return abs(area) * 0.5


def debug(*args):
    if False:
        print(args)


EPS = 1 / 10 ** 6


def intersect(line1, line2):
    x1, y1 = line1[0]
    x2, y2 = line1[1]

    x3, y3 = line2[0]
    x4, y4 = line2[1]

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if denominator == 0:
        1/0

    x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
    y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator

    return x, y


def solve():
    cnt, water_tall = map(float, input().split())
    cnt = int(cnt)

    points = []
    MAX = 10 ** 18

    for _ in range(cnt + 1):
        x, y = map(float, input().split())
        if not points:
            points.append((x, MAX))
        points.append((x, y))
    points.append((points[-1][0], MAX))

    wide = points[-1][0] - points[0][0]
    water_area = water_tall * wide
    waters = [0]
    for pos in range(1, cnt + 1):
        left = points[pos][0]
        right = points[pos + 1][0]
        size = abs(right - left)
        waters.append(water_area * (size / wide))
    waters.append(0)

    water2points = [0] * len(points)


    for pos, wat in enumerate(waters):
        if wat:
            left = points[pos][1]
            right = points[pos + 1][1]
            if left < right:
                water2points[pos] += wat
            else:
                water2points[pos + 1] += wat

    moved = True
    while moved:
        moved = False
        for pos, wat in enumerate(water2points):
            if wat:
                left = points[pos - 1][1]
                mid = points[pos][1]
                right = points[pos + 1][1]
                if left < mid:
                    water2points[pos] = 0
                    water2points[pos - 1] += wat
                    moved = True
                elif mid > right:
                    water2points[pos] = 0
                    water2points[pos + 1] += wat
                    moved = True


    #waters = [0] + [1] * cnt + [0]
    debug("waters", water_area, waters)
    debug("w2p", water2points)
    debug("points", points)

    result = -1

    stack = [(1, cnt + 1)]
    while stack:
        left_bound, right_bound = stack.pop()
        debug("step", left_bound, right_bound, "waters", water2points)


        if left_bound == right_bound:
            if not water2points[left_bound]:
                1/0
            max_pos = left_bound

            water = water2points[left_bound]

            left = points[max_pos][1]

            left_wall = points[left_bound -1]
            right_wall = points[right_bound + 1]
            left_line = (left_wall, points[max_pos])
            right_line = (points[max_pos], right_wall)

            #right = max(left_wall[1], right_wall[1])
            #right = water
            right = 10 ** 18

            debug("my water", water, (left, right))

            while  (right - left) > EPS:
                tall = (left + right) / 2


                hat = [
                    (left_wall[0], tall),
                    (right_wall[0], tall)
                ]

                left_inter = intersect(hat, left_line)
                right_inter = intersect(hat, right_line)
                subpoints = [
                    left_inter,
                    points[max_pos],
                    right_inter,
                    # new hat
                    # (right_inter[0], tall),
                    # (left_inter[0], tall),

                ]
                area = get_shoelace_area(subpoints)
                debug("check", tall, "area", area, subpoints)

                if area <= water:
                    left = tall + EPS
                else:
                    right = tall - EPS
            left -= points[max_pos][1]
            result = max(result, left)
            debug("tall is", left, points[max_pos][1])
        if left_bound >= right_bound:
            continue



        max_pos = max_tall = float('-inf')

        for pos in range(left_bound, right_bound + 1):
            y = points[pos][1]
            if y > max_tall:
                max_tall = y
                max_pos = pos

        debug("..I'm standing at", max_pos,  "tall", max_tall, "point", points[max_pos])
        left_water = right_water = left_area = right_area = 0
        if points[max_pos - 1][1] < max_tall:
            left_water = sum(water2points[left_bound: max_pos])


            left_point = points[left_bound - 1]
            left_wall = (left_point, points[left_bound])
            hat = [(left_point[0], max_tall), points[max_pos]]

            left_inter = intersect(left_wall, hat)

            subpoints = points[left_bound: max_pos + 1]
            subpoints.append(left_inter)
            #subpoints.append(points[max_pos])
            debug("left points", subpoints)
            left_area = get_shoelace_area(subpoints)

            debug("water left", left_water, "area left", left_area)

            if left_area > left_water:
                stack.append((left_bound, max_pos -1))

        if points[max_pos + 1][1] < max_tall:
            right_water = sum(
                water2points[max_pos + 1 : right_bound + 1]
            )


            right_wall = points[right_bound + 1]
            right_line = (points[right_bound], right_wall)
            hat = [
                points[max_pos],
                (right_wall[0], max_tall)
            ]

            right_inter = intersect(hat, right_line)

            subpoints = points[max_pos: right_bound + 1]
            subpoints.append(right_inter)
            debug("right points", subpoints)
            right_area = get_shoelace_area(subpoints)

            debug("water right", right_water, "area right", right_area)
            if right_area > right_water:
                stack.append((max_pos + 1, right_bound))



        water = (left_water + right_water) - (left_area + right_area)
        if water < 0:
            if left_water and left_area <= left_water:
                # left is drowning
                left_bottom = min(
                    x[1]
                    for x in points[left_bound : max_pos]
                )
                it = max_tall - left_bottom

                result = max(result, it)

                spill_over = left_water - left_area

                debug("left drowning", left_bottom, it, "spill", spill_over)

                for pos in range(max_pos + 1, len(water2points)):
                    if water2points[pos]:
                        water2points[pos] += spill_over
                        break

            if right_water and right_area <= right_water:
                # right is drowning
                right_bottom = min(
                    x[1]
                    for x in points[max_pos + 1: right_bound + 1]
                )
                it = max_tall - right_bottom

                result = max(result, it)

                spill_over = right_water - right_area
                debug("right drowning", right_bottom, it, "spill", spill_over)

                for pos in reversed(range(max_pos)):
                    if water2points[pos]:
                        water2points[pos] += spill_over
                        break
        else:
            # i'm drowning
            bottom = max_tall - min(
                x[1]
                for x in points[left_bound : right_bound + 1]
            )


            left = max_tall

            left_wall = points[left_bound - 1]
            right_wall = points[right_bound + 1]
            left_line = (left_wall, points[left_bound])
            right_line = (points[right_bound ], right_wall)

            bottom_line = (
                (left_wall[0] - 1,max_tall),
                (right_wall[0] + 1,max_tall),
            )

            left_bottom = intersect(left_line, bottom_line)
            right_bottom = intersect(bottom_line, right_line)

            #right = water
            right = 10 ** 18

            debug("my2 water", "me tall", max_tall, "rem water", water, bottom, "right", right)

            while  (right - left) > EPS:
                tall = (left + right) / 2


                hat = [
                    (left_wall[0] - 1, tall),
                    (right_wall[0] + 1, tall)
                ]

                left_inter = intersect(hat, left_line)
                right_inter = intersect(hat, right_line)
                subpoints = [
                    left_inter,
                    left_bottom,
                    right_bottom,
                    right_inter,
                    # new hat
                    # (right_inter[0], tall),
                    # (left_inter[0], tall),

                ]
                area = get_shoelace_area(subpoints)
                #print("check", tall, "area", area, "water", water, subpoints)

                if area <= water:
                    left = tall + EPS
                else:
                    right = tall - EPS


            debug("a", left, "bottom", bottom, "minus", max_tall, "plus", abs(bottom))
            left -= max_tall
            left += abs(bottom)
            result = max(result, left)
            debug("tall is", left, bottom)



    return result



print(solve())
