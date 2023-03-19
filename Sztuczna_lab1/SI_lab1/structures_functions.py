import heapq
import itertools
import math
from datetime import datetime
from re import T
from typing import Optional

"""
    Structures:
        - Graph
        - Priority Queue
"""


class Graph:
    def __init__(self):
        self.edges: dict[(str, str), (datetime.time, int, str, datetime.time)] = {}
        self.verticles: dict[str, list[str]] = {}
        self.width_height: dict[str, (float, float)] = {}

    def neighbors(self, id: str) -> list[str]:
        return self.verticles[id]

    """
        Time cost in minutes
        Fast version, exercise 1D
        Time improvment for searching in B
        for loop        = 0,67 [s]
        binary search   = 0,24 [s]
    """

    def cost_time(self, from_stop: str, to_stop: str, actual_time: datetime.time) -> \
            (int, (str, datetime.time, datetime.time)):
        all_edges = self.edges[from_stop, to_stop]
        index = binary_search(all_edges, 0, len(all_edges) - 1, actual_time)
        if index != -1:
            e = all_edges[index]
            return e[1] - time_diff(actual_time, e[0]), (e[2], e[0], e[3])
        else:
            return None

        # -------------- Old slow version ---------------------------
        # for e in self.edges[(from_stop, to_stop)]:
        #     if e[0] >= actual_time:
        #         return e[1] - time_diff(actual_time, e[0]), (e[2], e[0], e[3])
        # return None

    """
        Time cost in lines
        Fast version, exercise 1D

        Time improvement for searching in C
        for loop        = 0,51 [s]
        binary search   = 0,14 [s]
    """

    def cost_lines(self, from_stop: str, to_stop: str, actual_time: datetime.time, line: str) -> \
            (int, (str, datetime.time, datetime.time)):
        all_edges = self.edges[from_stop, to_stop]
        index = binary_search(all_edges, 0, len(all_edges) - 1, actual_time)
        if index != -1:
            e = all_edges[index]
            if e[2] == line:
                return e[1] - time_diff(actual_time, e[0]), (e[2], e[0], e[3])
            else:
                return e[1] - time_diff(actual_time, e[0]) + 600, (e[2], e[0], e[3])
        else:
            return None

        # -------------- Old slow version ---------------------------
        # for e in self.edges[(from_stop, to_stop)]:
        #     if e[0] >= actual_time:
        #         if e[2] == line:
        #             return e[1] - time_diff(actual_time, e[0]), (e[2], e[0], e[3])
        #         else:
        #             return e[1] - time_diff(actual_time, e[0]) + 600, (e[2], e[0], e[3])
        # return None


class PriorityQueue:
    def __init__(self):
        self.elements: list[tuple[float, T]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> T:
        return heapq.heappop(self.elements)[1]


"""
    Helper functions:
        - binary_search
        - heuristic (for A*)
        - reconstruct_path
        - time_diff
"""


def binary_search(arr, low, high, x):
    if high >= low:
        mid = (high + low) // 2
        if arr[mid][0] == x:
            return mid
        elif arr[mid][0] > x:
            return binary_search(arr, low, mid - 1, x)
        else:
            return binary_search(arr, mid + 1, high, x)
    else:
        if low >= len(arr):
            return -1
        if arr[low][0] > x:
            return low
        else:
            return -1


def heurisitc(graph, current, next):
    try:
        return \
                abs(graph.width_height[current][0] - graph.width_height[next][0]) + \
                abs(graph.width_height[current][1] - graph.width_height[next][1])
    except KeyError:
        return 0.0


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

    lines.reverse()
    lines.append(came_from[goal][1])
    return path, lines


def time_diff(to_time, from_time):
    return (to_time.hour * 60 + to_time.minute) - (from_time.hour * 60 + from_time.minute)


"""
    Exercise 1:
    a) Dijkstra
    b) A* time
    c) A* lines
    d) Binary search
"""


def dijkstra_search(graph: Graph, start: str, goal: str, actual_time: datetime.time):
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
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current, cost_with_route[1]
                time_so_far[next] = cost_with_route[1][2]

    return came_from, cost_so_far


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


"""
    Exercise 2
    a) Tabu search without limits
"""


def find_solution_time(graph: Graph, start: str, goals: list[str], actual_time: datetime.time):
    actual = start
    now_time = actual_time
    for stop in goals:
        came_from, cost = a_star_time(graph, actual, stop, now_time)
        path, lines = reconstruct_path(came_from, actual, stop)
        print(str(path) + ' ==== ' + str(lines))
        actual = stop
        now_time = lines[len(lines) - 2][2]

    came_from_start, cost = a_star_time(graph, actual, start, now_time)
    path_back, lines = reconstruct_path(came_from_start, actual, start)
    now_time = lines[len(lines) - 2][2]

    result = time_diff(now_time, actual_time)
    print(str(path_back) + ' ==== ' + str(lines))
    print('Solution time: ' + str(result) + '\n')
    return result


def find_solution_lines(graph: Graph, start: str, goals: list[str], actual_time: datetime.time):
    actual = start
    now_time = actual_time
    for stop in goals:
        came_from, cost = a_star_lines(graph, actual, stop, now_time)
        path, lines = reconstruct_path(came_from, actual, stop)
        print(str(path) + ' ==== ' + str(lines))
        actual = stop
        now_time = lines[len(lines) - 2][2]

    came_from_start, cost = a_star_lines(graph, actual, start, now_time)
    path_back, lines = reconstruct_path(came_from_start, actual, start)
    now_time = lines[len(lines) - 2][2]

    result = time_diff(now_time, actual_time)
    print(str(path_back) + ' ==== ' + str(lines))
    print('Solution lines: ' + result + '\n')
    return result


def get_best_neighbour_without_limits(
        graph: Graph,
        start: str, goals: list[str],
        tabu_history, tabu_limit: int, aspiration: int,
        actual_time: datetime.time,
        by_time: bool
):
    best_neighbour = None
    best_neighbour_cost = math.inf

    possibilities = list(itertools.permutations(goals, len(goals)))
    for route in possibilities:

        # Take a route and decide which cost
        if by_time:
            actual_solution = find_solution_time(graph, start, list(route), actual_time)
        else:
            actual_solution = find_solution_lines(graph, start, list(route), actual_time)

        # This route is tabu
        if route in tabu_history:
            if tabu_history[route] > 0:
                continue

        if actual_solution < best_neighbour_cost:
            best_neighbour_cost = actual_solution
            best_neighbour = route
            tabu_history[best_neighbour] = tabu_limit

    return best_neighbour, best_neighbour_cost


def tabu_search_without_limits(
    graph: Graph,
    start, goals, actual_time,
    num_iter,
    tabu_limit, tabu_history, aspiration,
    by_time
):
    best_solution = goals
    if by_time:
        best_cost = find_solution_time(graph, start, best_solution, actual_time)
    else:
        best_cost = find_solution_lines(graph, start, best_solution, actual_time)
    states = [best_cost]

    historical_best = best_solution
    historical_best_cost = best_cost

    for _ in range(num_iter):
        # Reduce counter for all tabu
        for x in tabu_history:
            tabu_history[x] -= 1
        tabu_history = {x: tabu_history[x] for x in tabu_history if tabu_history[x] > 0}

        best_solution, best_cost = get_best_neighbour_without_limits(
            graph,
            start, goals,
            tabu_history, tabu_limit, aspiration,
            actual_time, by_time
        )

        if best_cost <= historical_best_cost:
            historical_best = best_solution
            historical_best_cost = best_cost
        states.append(best_cost)
    return historical_best, historical_best_cost, states
