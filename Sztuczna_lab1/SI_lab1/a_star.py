import datetime
import time

import pandas as pd

from structures_functions import Graph, time_diff, a_star_time, reconstruct_path, a_star_lines

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

    stops, lines = reconstruct_path(came_from, values[0], values[1])
    result = zip(stops, lines)

    print("Route")
    for route_part in result:
        print('      - ' + str(route_part))

    print('Czas przejazdu: ' + str(cost[values[1]]) + ' [min]')
    print('Czas działania programu: ' + str(round(end_time - start_time, 2)) + ' [s]\n')

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

    stops, lines = reconstruct_path(came_from, values[0], values[1])
    amount_of_lines = len(list(set(map(lambda l: l[0], lines[1:len(lines) - 1]))))
    result = zip(stops, lines)

    print("Route")
    for route_part in result:
        print('      - ' + str(route_part))

    print('Czas przejazdu: ' + str(cost[values[1]] - 600 * amount_of_lines) + ' min')
    print('Czas działania ' + str(round(end_time - start_time, 2)) + ' [s]')
    print('Ilość przesiadek: ' + str(amount_of_lines - 1))
