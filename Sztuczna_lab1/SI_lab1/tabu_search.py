# import datetime
# import heapq
# import math
# from re import T
# from typing import Optional
#
# import pandas as pd
# #
# #
# # def binary_search(arr, low, high, x):
# #     if high >= low:
# #         mid = (high + low) // 2
# #         if arr[mid][0] == x:
# #             return mid
# #         elif arr[mid][0] > x:
# #             return binary_search(arr, low, mid - 1, x)
# #         else:
# #             return binary_search(arr, mid + 1, high, x)
# #     else:
# #         if low >= len(arr):
# #             return -1
# #         if arr[low][0] > x:
# #             return low
# #         else:
# #             return -1
# #
# #
# # class Graph:
# #     def __init__(self):
# #         self.edges: dict[(str, str), (datetime.time, int, str, datetime.time)] = {}
# #         self.verticles: dict[str, list[str]] = {}
# #         self.width_height: dict[str, (float, float)] = {}
# #
# #     def neighbors(self, id: str) -> list[str]:
# #         return self.verticles[id]
# #
# #     def cost_time(self, from_stop: str, to_stop: str, actual_time: datetime.time) -> \
# #             (int, (str, datetime.time, datetime.time)):
# #         all_edges = self.edges[from_stop, to_stop]
# #         index = binary_search(
# #             all_edges,
# #             0,
# #             len(all_edges) - 1,
# #             actual_time
# #         )
# #         if index != -1:
# #             e = all_edges[index]
# #             return e[1] - time_diff(actual_time, e[0]), (e[2], e[0], e[3])
# #         else:
# #             return None
# #
# #     # Time cost in lines
# #     def cost_lines(self, from_stop: str, to_stop: str, actual_time: datetime.time, line: str) -> \
# #             (int, (str, datetime.time, datetime.time)):
# #         for e in self.edges[(from_stop, to_stop)]:
# #             if e[0] >= actual_time:
# #                 if e[2] == line:
# #                     return e[1] - time_diff(actual_time, e[0]), (e[2], e[0], e[3])
# #                 else:
# #                     return e[1] - time_diff(actual_time, e[0]) + 600, (e[2], e[0], e[3])
# #         return None
# #
# #
# # def a_star_time(graph: Graph, start: str, goal: str, actual_time: datetime.time):
# #     frontier = PriorityQueue()
# #     frontier.put(start, 0)
# #
# #     came_from: dict[str, (Optional[str], (str, datetime.time))] = {}
# #     cost_so_far: dict[str, float] = {}
# #     time_so_far: dict[str, datetime.time] = {}
# #
# #     came_from[start] = None
# #     cost_so_far[start] = 0
# #     time_so_far[start] = actual_time
# #
# #     while not frontier.empty():
# #         current: str = frontier.get()
# #
# #         if current == goal:
# #             break
# #
# #         try:
# #             graph.neighbors(current)
# #         except KeyError:
# #             continue
# #
# #         for next in graph.neighbors(current):
# #             cost_with_route = graph.cost_time(current, next, time_so_far[current])
# #             if cost_with_route is None:
# #                 continue
# #             new_cost = cost_so_far[current] + cost_with_route[0]
# #
# #             if next not in cost_so_far or new_cost < cost_so_far[next]:
# #                 cost_so_far[next] = new_cost
# #                 priority = new_cost
# #                 frontier.put(next, priority)
# #                 came_from[next] = current, cost_with_route[1]
# #                 time_so_far[next] = cost_with_route[1][2]
# #
# #     return came_from, cost_so_far
# #
# #
# # class PriorityQueue:
# #     def __init__(self):
# #         self.elements: list[tuple[float, T]] = []
# #
# #     def empty(self) -> bool:
# #         return not self.elements
# #
# #     def put(self, item: T, priority: float):
# #         heapq.heappush(self.elements, (priority, item))
# #
# #     def get(self) -> T:
# #         return heapq.heappop(self.elements)[1]
# #
# #
# # def time_diff(to_time, from_time):
# #     return (to_time.hour * 60 + to_time.minute) - (from_time.hour * 60 + from_time.minute)
# #
# # def reconstruct_path(came_from: dict[str, str], start: str, goal: str) -> \
# #         (list[str], list[(str, datetime.time, datetime.time)]):
# #     current: str = goal
# #     path: list[str] = []
# #     lines: list[(str, datetime.time, datetime.time)] = []
# #     if goal not in came_from:  # no path was found
# #         return []
# #
# #     while current != start:
# #         path.append(current)
# #         current = came_from[current][0]
# #         if current != start:
# #             lines.append(came_from[current][1])
# #     path.append(start)
# #     path.reverse()
# #
# #     lines.append(start)
# #     lines.reverse()
# #     lines.append(goal)
# #     return path, lines
#
#
# def find_solution_time(graph: Graph, start: str, goals: list[str], actual_time: datetime.time):
#     actual = start
#     now_time = actual_time
#     for stop in goals:
#         came_from, cost = a_star_time(graph, actual, stop, now_time)
#         path, lines = reconstruct_path(came_from, actual, stop)
#         print(str(path) + ' ==== ' + str(lines))
#         actual = stop
#         now_time = lines[len(lines) - 2][2]
#
#     came_from_start, cost = a_star_time(graph, actual, start, now_time)
#     path_back, lines = reconstruct_path(came_from_start, actual, start)
#     now_time = lines[len(lines) - 2][2]
#     print(str(path_back) + ' ==== ' + str(lines))
#
#     return time_diff(now_time, actual_time)
#
#
# def tabu_search(graph: Graph, start: str, goals: list[str], actual_time: datetime.time):
#     initial_solution = find_solution_time(graph, start, goals, actual_time)
#     print(initial_solution)
#
#
#
#
# if __name__ == '__main__':
#     df = pd.read_csv(
#         'connection_graph.csv',
#         parse_dates=['departure_time', 'arrival_time'],
#         date_parser=lambda x: pd.to_datetime(x, format='%H:%M:%S').time
#     )
#
#     """
#         Reading from file:
#         [0] - Unnamed
#         [1] - ID
#         [2] - Company
#         [3] - Line
#         [4, 5] - time from /to
#         [6, 7] - start / end stop
#         [8, 9] - width / height start stop
#         [10, 11] - width / height end stop
#     """
#
#     city_map = Graph()
#
#     for row in df.values:
#         stop_from = str(row[6]).lower()
#         from_w_h = row[8], row[9]
#
#         stop_to = str(row[7]).lower()
#
#         if stop_from in city_map.verticles.keys():
#             city_map.verticles[stop_from].append(stop_to)
#         else:
#             city_map.verticles[stop_from] = [stop_to]
#             city_map.width_height[stop_from] = from_w_h
#
#         edge = row[4], time_diff(row[5], row[4]), row[3], row[5]
#         if (stop_from, stop_to) in city_map.edges.keys():
#             city_map.edges[(stop_from, stop_to)].append(edge)
#         else:
#             city_map.edges[(stop_from, stop_to)] = [edge]
#
#     """
#     Example data:
#     [('krzyki', 'sowia)] -> [
#         (datetime.time(17, 3), 1, 'A', datetime(17, 4))
#         (datetime.time(17, 18), 1, 'A', dateime(17, 19))
#         (datetime.time(17, 16), 2, 'D', datetime(17, 17)
#         etc.
#     ]
#     """
#
#     """
#         Sorting by time
#     """
#     for r in city_map.edges.values():
#         r.sort(key=lambda x: x[0])
#
#     tabu_search(
#         city_map,
#         'kurpiów',
#         ['krzyki', 'dworzec główny', 'przyjaźni'],
#         datetime.time(12, 15, 00)
#     )
