import datetime
import time

import pandas as pd

from structures_functions import Graph, time_diff, dijkstra_search, reconstruct_path

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
        stop_to = str(row[7]).lower()
        if stop_from in city_map.verticles.keys():
            city_map.verticles[stop_from].append(stop_to)
        else:
            city_map.verticles[stop_from] = [stop_to]

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
        Exercise 1 - Dijkstra algorithm by time
    """
    start_time = time.time()

    values = ('grota-roweckiego', 'pl. grunwaldzki', datetime.time(12, 15, 0))

    came_from, cost = dijkstra_search(
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
