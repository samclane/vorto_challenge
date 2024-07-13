import csv
import math
from typing import Any, List, Dict, Set
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
    def from_str(cls, s: str) -> "Point":
        x, y = s.strip("()").split(",")
        return cls(float(x), float(y))

    def distance(self, other: "Point"):
        return distance_between_points(self, other)


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

    def __hash__(self) -> int:
        return hash(self.id)


class Route:
    def __init__(self, loads: List[Load]):
        self.loads = loads
        self.time = self.calculate_time()

    def calculate_time(self) -> float:
        """Calculate route time, including return to DEPOT trip"""
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


def find_nearest_load(remaining_loads: Set[Load], current_pos: Point) -> Load:
    return min(remaining_loads, key=lambda l: current_pos.distance(l.pickup))


def nearest_neighbor_multiple_salesmen(loads: List[Load]) -> List[Route]:
    # All unique loads
    remaining_loads = set(loads)
    routes: List[Route] = []

    while remaining_loads:
        # New Driver/Route
        current_pos = DEPOT
        route_loads: List[Load] = []
        while remaining_loads:
            # Get nearest neighbor
            next_load = find_nearest_load(remaining_loads, current_pos)
            # Check if route can be made without exceeding time
            if Route(route_loads + [next_load]).calculate_time() <= MAX_TIME:
                route_loads.append(next_load)
                current_pos = next_load.dropoff
                remaining_loads.remove(next_load)
            else:
                break
        if route_loads:
            routes.append(Route(route_loads))
        else:
            break
    
    return routes


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

    routes = nearest_neighbor_multiple_salesmen(loads)
    solution = Solution(routes)
    return solution


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("problemFile", help="File to process")
    args = parser.parse_args()
    solution = solve(args.problemFile)
    print(solution)
