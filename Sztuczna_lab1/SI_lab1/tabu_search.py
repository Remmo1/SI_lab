import datetime

import pandas as pd

import structures_functions
from structures_functions import Graph, time_diff, tabu_search_without_limits

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
        Exercise 1:
        Tabu search without limits (take every possible path)
    """

    best_route = tabu_search_without_limits(
        city_map,
        'kurpiów',
        ['krzyki', 'dworzec główny', 'przyjaźni'],
        datetime.time(12, 15, 00),
        True
    )
    print('Best: ' + str(best_route))
