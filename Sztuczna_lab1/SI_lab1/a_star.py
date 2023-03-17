import datetime
import heapq
from re import T
import time
from typing import Optional

import pandas as pd


class Graph:
    def __init__(self):
        self.edges: dict[(str, str), (datetime.time, int, str, datetime.time)] = {}
        self.verticles: dict[str, list[str]] = {}
        self.width_height: dict[str, (float, float)] = {}

    def neighbors(self, id: str) -> list[str]:
        return self.verticles[id]

    # Time cost in minutes
    def cost_time(self, from_stop: str, to_stop: str, actual_time: datetime.time) -> \
            (int, (str, datetime.time, datetime.time)):
        for e in self.edges[(from_stop, to_stop)]:
            if e[0] >= actual_time:
                return e[1] - time_diff(actual_time, e[0]), (e[2], e[0], e[3])
        return None

    # Time cost in lines
    def cost_lines(self, from_stop: str, to_stop: str, actual_time: datetime.time, line: str) -> \
            (int, (str, datetime.time, datetime.time)):
        for e in self.edges[(from_stop, to_stop)]:
            if e[0] >= actual_time:
                if e[2] == line:
                    return e[1] - time_diff(actual_time, e[0]), (e[2], e[0], e[3])
                else:
                    return e[1] - time_diff(actual_time, e[0]) + 600, (e[2], e[0], e[3])
        return None


class PriorityQueue:
    def __init__(self):
        self.elements: list[tuple[float, T]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> T:
        return heapq.heappop(self.elements)[1]


def heurisitc(graph, current, next):
    try:
        return \
                abs(graph.width_height[current][0] - graph.width_height[next][0]) + \
                abs(graph.width_height[current][1] - graph.width_height[next][1])
    except KeyError:
        return 0.0


def a_star_time(graph: Graph, start: str, goal: str, actual_time: datetime.time):
    frontier = PriorityQueue()
    frontier.put(start, 0)

    came_from: dict[str, (Optional[str], (str, datetime.time))] = {}
    cost_so_far: dict[str, float] = {}
    time_so_far: dict[str, datetime.time] = {}

    came_from[start] = None
    cost_so_far[start] = 0
    time_so_far[start] = actual_time

    while not frontier.empty():
        current: str = frontier.get()

        if current == goal:
            break

        try:
            graph.neighbors(current)
        except KeyError:
            continue

        for next in graph.neighbors(current):
            cost_with_route = graph.cost_time(current, next, time_so_far[current])
            if cost_with_route is None:
                continue
            new_cost = cost_so_far[current] + cost_with_route[0]

            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heurisitc(graph, current, next)
                frontier.put(next, priority)
                came_from[next] = current, cost_with_route[1]
                time_so_far[next] = cost_with_route[1][2]

    return came_from, cost_so_far


def a_star_lines(graph: Graph, start: str, goal: str, actual_time: datetime.time):
    frontier = PriorityQueue()
    frontier.put(start, 0)

    came_from: dict[str, (Optional[str], (str, datetime.time))] = {}
    cost_so_far: dict[str, float] = {}
    time_so_far: dict[str, datetime.time] = {}
    line_so_far: dict[str, str] = {}

    came_from[start] = None
    cost_so_far[start] = 0
    time_so_far[start] = actual_time
    line_so_far[start] = ""

    while not frontier.empty():
        current: str = frontier.get()

        if current == goal:
            break

        try:
            graph.neighbors(current)
        except KeyError:
            continue

        for next in graph.neighbors(current):
            cost_with_route = graph.cost_lines(current, next, time_so_far[current], line_so_far[current])
            if cost_with_route is None:
                continue
            new_cost = cost_so_far[current] + cost_with_route[0]

            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heurisitc(graph, current, next)
                frontier.put(next, priority)
                came_from[next] = current, cost_with_route[1]
                time_so_far[next] = cost_with_route[1][2]
                line_so_far[next] = cost_with_route[1][0]

    return came_from, cost_so_far


def time_diff(to_time, from_time):
    return (to_time.hour * 60 + to_time.minute) - (from_time.hour * 60 + from_time.minute)


def reconstruct_path(came_from: dict[str, str], start: str, goal: str) -> \
        (list[str], list[(str, datetime.time, datetime.time)]):
    current: str = goal
    path: list[str] = []
    lines: list[(str, datetime.time, datetime.time)] = []
    if goal not in came_from:  # no path was found
        return []

    while current != start:
        path.append(current)
        current = came_from[current][0]
        if current != start:
            lines.append(came_from[current][1])
    path.append(start)
    path.reverse()

    lines.append(start)
    lines.reverse()
    lines.append(goal)
    return path, lines

if __name__ == '__main__':
    df = pd.read_csv(
        'connection_graph.csv',
        parse_dates=['departure_time', 'arrival_time'],
        date_parser=lambda x: pd.to_datetime(x, format='%H:%M:%S').time
    )

    """
        Reading from file:
        [0] - Unnamed
        [1] - ID
        [2] - Company
        [3] - Line
        [4, 5] - time from /to
        [6, 7] - start / end stop
        [8, 9] - width / height start stop
        [10, 11] - width / height end stop 
    """

    city_map = Graph()

    for row in df.values:
        stop_from = str(row[6]).lower()
        from_w_h = row[8], row[9]

        stop_to = str(row[7]).lower()

        if stop_from in city_map.verticles.keys():
            city_map.verticles[stop_from].append(stop_to)
        else:
            city_map.verticles[stop_from] = [stop_to]
            city_map.width_height[stop_from] = from_w_h

        edge = row[4], time_diff(row[5], row[4]), row[3], row[5]
        if (stop_from, stop_to) in city_map.edges.keys():
            city_map.edges[(stop_from, stop_to)].append(edge)
        else:
            city_map.edges[(stop_from, stop_to)] = [edge]

    """
    Example data:
    [('krzyki', 'sowia)] -> [
        (datetime.time(17, 3), 1, 'A', datetime(17, 4))
        (datetime.time(17, 18), 1, 'A', dateime(17, 19))
        (datetime.time(17, 16), 2, 'D', datetime(17, 17)
        etc.
    ]
    """

    """
        Sorting by time
    """
    for r in city_map.edges.values():
        r.sort(key=lambda x: x[0])

    """
        Exercise 2 - A* algorithm by time
    """
    start_time = time.time()

    values = ('grota-roweckiego', 'pl. grunwaldzki', datetime.time(12, 15, 0))

    came_from, cost = a_star_time(
        city_map,
        values[0],
        values[1],
        values[2]
    )
    end_time = time.time()

    path = reconstruct_path(came_from, values[0], values[1])
    print(path[0])
    print(path[1])
    print(str(cost[values[1]]) + ' min')
    print('Czas działania ' + str(round(end_time - start_time, 2)) + ' [s]')

    """
            Exercise 3 - A* algorithm by lines
    """
    start_time = time.time()

    values = ('grota-roweckiego', 'pl. grunwaldzki', datetime.time(16, 18, 0))

    came_from, cost = a_star_lines(
        city_map,
        values[0],
        values[1],
        values[2]
    )
    end_time = time.time()

    path, lines = reconstruct_path(came_from, values[0], values[1])
    amount_of_lines = len(list(set(map(lambda l: l[0], lines[1:len(lines) - 1]))))
    print(path)
    print(lines)
    print('Czas przejazdu: ' + str(cost[values[1]] - 600 * amount_of_lines) + ' min')
    print('Czas działania ' + str(round(end_time - start_time, 2)) + ' [s]')
    print('Ilość przesiadek: ' + str(amount_of_lines - 1))
