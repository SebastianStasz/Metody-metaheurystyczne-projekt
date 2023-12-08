from cities import cities
from distances import get_distances_between_cities

number_of_cars = 5
car_capacity = 1000

if __name__ == '__main__':
    distances_matrix = get_distances_between_cities(cities)
    number_of_clients = len(cities)
    total_demand = 0
    
    for city in cities:
        total_demand += city["demand"]

    print(f'Number of clients: {number_of_clients}')
    print(f'Total demand: {total_demand}')
    print(distances_matrix)
