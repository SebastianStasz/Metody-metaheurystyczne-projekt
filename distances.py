import pandas as pd
from math import sin, cos, sqrt, atan2, radians
from scipy.spatial.distance import pdist, squareform


def distance_between_coordinates(x, y):
    lat1 = radians(x[0])
    lon1 = radians(x[1])
    lat2 = radians(y[0])
    lon2 = radians(y[1])

    R = 6373.0
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return round(distance, 4)


def get_distances_between_cities(cities):
    lattitude = []
    longtitude = []

    for city in cities:
        lattitude.append(city["coordinates"]["x"])
        longtitude.append(city["coordinates"]["y"])

    lat_long = pd.DataFrame({'lattitude': lattitude, 'longtitude': longtitude})

    distances = pdist(lat_long.values, metric=distance_between_coordinates)

    points = [f'point_{i}' for i in range(1, len(lat_long) + 1)]

    df_distance = pd.DataFrame(squareform(distances), columns=points, index=points)
    return df_distance
