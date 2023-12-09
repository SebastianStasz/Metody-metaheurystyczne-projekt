from cities import cities
from distances import get_distances_between_cities
from AntColony import AntColony
import numpy as np


def get_cars_by_highest_capacity(cities):
    cities_by_demand = sorted(cities, key=lambda x: x["demand"], reverse=True)
    cars = []
    
    for car_number in [1, 2, 3, 4, 5]:
        capacity = 0
        cities = []

        if car_number == 5:
            capacity = sum(city["demand"] for city in cities_by_demand)
            car = {"number": car_number, "cities": cities_by_demand, "used_capacity": capacity}
            cars.append(car)
            break
        
        for city in cities_by_demand:
            new_capacity = capacity + city["demand"]
            
            if new_capacity <= 1000:
                cities_by_demand.remove(city)
                capacity = new_capacity
                cities.append(city)

        car = {"number": car_number, "cities": cities, "used_capacity": capacity}
        cars.append(car)
    
    return cars


if __name__ == '__main__':
    cars = get_cars_by_highest_capacity(cities)
    paths = []

    for car in cars:
        distances_matrix = get_distances_between_cities(car["cities"])
        ant_colony = AntColony(np.array(distances_matrix), 5, 1, 100, 0.95, alpha=1, beta=1)
        shortest_path = ant_colony.run()
        paths.append(shortest_path)
        print(f'Path: {shortest_path}')
    
    total_distance = sum(path[1] for path in paths)
        
    print(f'Total distance: {total_distance} km')
