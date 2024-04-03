from dataclasses import dataclass
from itertools import pairwise


@dataclass
class Point:
    x: float
    y: float


class Lake:
    EPS = 0.1**7

    def __init__(self, points, H=None, water=None, next=None, max_peek=None):
        self.l_side = points[0]
        self.r_side = points[-1]
        self.bot = min(points, key=lambda a: a.y)
        self.max_peek = max_peek
        self.next = next
        self.points = points
        self.volume = None

        if water is None:
            self.water = (self.r_side.x - self.l_side.x) * H
        else:
            self.water = water

        self.init_volume()

    def init_volume(self):
        self.volume = self.get_volume_on_mirror(min(self.r_side.y, self.l_side.y))

    def is_falling_left(self):
        return self.l_side.y < self.r_side.y

    def is_overfilled(self):
        return self.water > self.volume

    def take_slurps(self, other):
        self.water += other.water - other.volume
        other.water = other.volume

    def get_depth(self):
        return self.get_mirror() - self.bot.y

    def get_mirror(self):
        if self.volume == self.water:
            return min(self.l_side.y, self.r_side.y)
        if self.max_peek is None:
            l = self.bot.y + self.EPS
        else:
            l = self.max_peek.y + self.EPS
        r = min(self.l_side.y, self.r_side.y) - self.EPS
        return self.bs(l, r)

    def bs(self, l, r):
        while l + self.EPS < r:
            m = (l + r) / 2
            if self.get_volume_on_mirror(m) > self.water:
                r = m
            else:
                l = m
        return l

    @staticmethod
    def interpolate(p1, p2, mirror):
        if p1.x == p2.x or p1.y == mirror:
            mirror_p_x = p1.x
        elif p2.y == mirror:
            mirror_p_x = p2.x
        else:
            dx = p1.x - p2.x
            dy = p1.y - p2.y
            mirror_p_x = dx * (mirror - p1.y) / dy + p1.x
        return Point(mirror_p_x, mirror)

    def get_volume_on_mirror(self, mirror):
        points = self.points

        i = 0
        while points[i + 1].y > mirror:
            i += 1
        start = self.interpolate(points[i], points[i + 1], mirror)

        j = -1
        while points[j - 1].y > mirror:
            j -= 1
        end = self.interpolate(points[j], points[j - 1], mirror)

        return self.calculate_volume([start] + points[i + 1:j] + [end, start])

    @staticmethod
    def calculate_volume(points):
        return abs(sum(p1.x * p2.y for p1, p2 in pairwise(points))
                   - sum(p1.y * p2.x for p1, p2 in pairwise(points))) / 2


class LinkedLakes:
    def __init__(self, points, N, H):
        self.head = None
        self.init_lakes(points, N, H)

    def init_lakes(self, points, N, H):
        curr_points = []
        curr_lake = None
        for i in range(N + 3):
            curr_points.append(points[i])
            if i != 0 and (i == N + 2 or points[i - 1].y < points[i].y > points[i + 1].y):
                if curr_lake is None:
                    self.head = curr_lake = Lake(curr_points, H)
                else:
                    curr_lake.next = Lake(curr_points, H)
                    curr_lake = curr_lake.next
                curr_points = [points[i]]

    def get_min_depth(self):
        curr = self.head
        max_depth = 0
        while curr:
            max_depth = max(curr.get_depth(), max_depth)
            curr = curr.next
        return max_depth

    def solve(self):
        while True:
            if self.balance():
                break
        print(self.get_min_depth())

    def balance(self):
        prev_lake = None
        curr_lake = self.head
        balanced = True
        while curr_lake and curr_lake.next:
            next_lake = curr_lake.next

            if curr_lake.is_overfilled() and not curr_lake.is_falling_left():
                balanced = False
                next_lake.take_slurps(curr_lake)
                if next_lake.is_falling_left() and next_lake.is_overfilled():
                    curr_lake = self.merge_lakes(curr_lake, next_lake, prev_lake)

            elif next_lake.is_overfilled() and next_lake.is_falling_left():
                balanced = False
                curr_lake.take_slurps(next_lake)
                if not curr_lake.is_falling_left() and curr_lake.is_overfilled():
                    curr_lake = self.merge_lakes(curr_lake, next_lake, prev_lake)

            prev_lake, curr_lake = curr_lake, curr_lake.next
        return balanced

    def merge_lakes(self, l_lake, r_lake, prev_lake):
        new_points = l_lake.points + r_lake.points[1:]
        new_water = l_lake.water + r_lake.water
        max_peek = l_lake.points[-1]
        new_lake = Lake(new_points, water=new_water, next=r_lake.next, max_peek=max_peek)
        if prev_lake:
            prev_lake.next = new_lake
        else:
            self.head = new_lake
        return new_lake


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        N, H = f.readline().strip().split()
        N, H = int(N), float(H)
        points = []
        for _ in range(N + 1):
            point = Point(*[int(i) for i in f.readline().strip().split()])
            if not points:
                points.append(Point(point.x, 10**10))
            points.append(point)
        points.append(Point(points[-1].x, 10**10))
        ll = LinkedLakes(points, N, H)
        ll.solve()
