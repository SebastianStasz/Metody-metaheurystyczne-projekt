import numpy as np
from geopy.distance import geodesic


def calculate_distances(latitude, longitude):
    n = len(latitude)
    distances = np.full((n, n), np.inf)

    for i in range(n):
        for j in range(n):
            if i != j:
                coord1 = (latitude[i], longitude[i])
                coord2 = (latitude[j], longitude[j])
                distance = geodesic(coord1, coord2).kilometers
                distances[i][j] = distance

    distances[distances == 0] = 0
    return distances


def get_distances_between_cities(cities):
    latitude = []
    longitude = []

    for city in cities:
        latitude.append(city["coordinates"]["x"])
        longitude.append(city["coordinates"]["y"])

    distances = calculate_distances(latitude, longitude)
    
    return distances
