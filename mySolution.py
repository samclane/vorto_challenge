import csv
from itertools import permutations
import math
from typing import Any, List, Dict
import argparse
from functools import lru_cache


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point(" + str(self.x) + "," + str(self.y) + ")"

    def __repr__(self) -> str:
        return "Point{}".format(str(self))

    @classmethod
    def from_str(cls, s: str) -> "Point":
        x, y = s.strip("()").split(",")
        return cls(float(x), float(y))

    def distance(self, other: "Point"):
        return distance_between_points(self, other)


@lru_cache(None)
def distance_between_points(p1: Point, p2: Point) -> float:
    xd = p1.x - p2.x
    yd = p1.y - p2.y
    return math.sqrt(xd * xd + yd * yd)


class Load:
    def __init__(self, _id: int, pickup: Point, dropoff: Point):
        self.id = _id
        self.pickup = pickup
        self.dropoff = dropoff

    def __str__(self):
        return f"Load({self.id} {self.pickup} {self.dropoff})"

    def __repr__(self) -> str:
        return f"Load({self.id} {self.pickup} {self.dropoff})"


class Route:
    def __init__(self, loads: List[Load]):
        self.loads = loads
        self.time = self.calculate_time()

    def calculate_time(self) -> float:
        pos = DEPOT
        t = 0
        for l in self.loads:
            t += pos.distance(l.pickup)
            t += l.pickup.distance(l.dropoff)
            pos = l.dropoff
        if pos != DEPOT:
            t += pos.distance(DEPOT)
        return t

    @property
    def is_valid(self) -> bool:
        return self.time < MAX_TIME

    def __str__(self) -> str:
        return f"[{','.join([str(l.id) for l in self.loads])}]"

    def __repr__(self) -> str:
        return f"Route({','.join([str(l.id) for l in self.loads])})"


class Solution:
    def __init__(self, routes: List[Route]):
        self.routes = routes
        self.is_valid: bool = all(r.is_valid for r in self.routes)
        self.cost: float = DRIVER_COST * self.num_drivers + sum(
            r.time for r in self.routes
        )

    @property
    def num_drivers(self) -> int:
        return len(self.routes)

    def __str__(self):
        return "\n".join(map(str, self.routes))

    def __repr__(self) -> str:
        return f"Solution({self.routes}, {self.cost}, {self.num_drivers})"

    def __getitem__(self, i) -> Route:
        return self.routes[i]


def read_file(path: str) -> List[Dict[str, Any]]:
    with open(path, "r") as f:
        reader = csv.DictReader(f, delimiter=" ")
        return list(reader)


def all_splits(lst):
    if len(lst) == 1:
        return [[lst]]
    result = []
    for i in range(1, len(lst)):
        left = lst[:i]
        right = lst[i:]
        result.append([left, right])
        for r in all_splits(right):
            result.append([left] + r)
    return result


def permute_loads(L):
    all_permutations = permutations(L)
    all_sublists = set()

    for perm in all_permutations:
        splits = all_splits(list(perm))
        for split in splits:
            all_sublists.add(tuple(map(tuple, split)))

    return [list(map(Route, sublist)) for sublist in all_sublists]


DRIVER_COST = 500
MAX_TIME = 12 * 60
DEPOT = Point(0, 0)


def solve(filename: str) -> Solution:
    loads = [
        Load(
            int(l["loadNumber"]),
            Point.from_str(l["pickup"]),
            Point.from_str(l["dropoff"]),
        )
        for l in read_file(filename)
    ]

    return min(
        [s for s in map(Solution, permute_loads(loads)) if s.is_valid],
        key=lambda s: s.cost,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--problemFile", help="File to process")
    args = parser.parse_args()
    solution = solve(args.problemFile)
    print(solution)
