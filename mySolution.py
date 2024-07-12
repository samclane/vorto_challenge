import csv
from itertools import permutations
import math
from typing import Any
import argparse


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point(" + str(self.x) + "," + str(self.y) + ")"

    def __repr__(self) -> str:
        return "Point{}".format(str(self))

    @classmethod
    def from_str(cls, s: str):
        x, y = s.strip("()").split(",")
        return cls(float(x), float(y))

    def distance(self, other: "Point"):
        return distance_between_points(self, other)


def distance_between_points(p1: Point, p2: Point) -> float:
    xDiff = p1.x - p2.x
    yDiff = p1.y - p2.y
    return math.sqrt(xDiff * xDiff + yDiff * yDiff)


class Load:
    def __init__(self, _id: int, pickup: Point, dropoff: Point):
        self.id = _id
        self.pickup = pickup
        self.dropoff = dropoff

    def __str__(self):
        return "Load({} {} {})".format(self.id, self.pickup, self.dropoff)

    def __repr__(self) -> str:
        return self.__str__()


class Route:
    def __init__(self, loads: list[Load]):
        self.loads = loads

        pos = DEPOT
        t = 0
        for l in self.loads:
            t += pos.distance(l.pickup)
            t += l.pickup.distance(l.dropoff)
            pos = l.dropoff
        t += pos.distance(DEPOT)

        self.time: float = t
        self.is_valid: bool = self.time < MAX_TIME

    def __str__(self) -> str:
        return "[{}]".format(",".join([str(l.id) for l in self.loads]))

    def __repr__(self) -> str:
        return "Route({})".format(",".join([str(l.id) for l in self.loads]))


class Solution:
    def __init__(self, routes: list[Route]):
        self.routes = routes
        self.is_valid: bool = all([r.is_valid for r in self.routes])
        self.cost: float = (DRIVER_COST * self.num_drivers) + sum(
            r.time for r in self.routes
        )

    @property
    def num_drivers(self) -> int:
        return len(self.routes)

    def __str__(self):
        return "\n".join(map(str, self.routes))

    def __repr__(self) -> str:
        return "Solution({}, {}, {})".format(self.routes, self.cost, self.num_drivers)

    def __getitem__(self, i) -> Route:
        return self.routes[i]


def read_file(path: str) -> list[dict[str, Any]]:
    with open(path, "r") as f:
        reader = csv.DictReader(f, delimiter=" ")
        return list(reader)


def permute_loads(L):
    # TODO: Get this to change route order as well
    def split(L):
        if not L:
            return [[]]
        result = []
        for i in range(1, len(L) + 1):
            first, rest = L[:i], L[i:]
            for sub in split(rest):
                result.append([first] + sub)
        return result

    sublists = split(L)
    all_permutations = []

    for sublist in sublists:
        all_permutations.extend(permutations(sublist))

    all_permutations = [list(map(Route, perm)) for perm in all_permutations]

    return all_permutations


DRIVER_COST = 500
MAX_TIME = 12 * 60
DEPOT = Point(0, 0)


def solve(filename: str) -> Solution:
    # print(args.problemFile)
    # print(read_file(args.problemFile))
    loads = [
        Load(
            int(l["loadNumber"]),
            Point.from_str(l["pickup"]),
            Point.from_str(l["dropoff"]),
        )
        for l in read_file(filename)
    ]
    # print(loads)

    sl = permute_loads(loads)
    solutions = [s for s in map(Solution, sl) if s.is_valid]
    solutions = sorted(solutions, key=lambda s: s.cost, reverse=False)
    print(solutions)
    return solutions[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--problemFile", help="File to process")
    args = parser.parse_args()
    solution = solve(args.problemFile)
    print(solution, solution.cost, solution.is_valid, solution[-1].time)
