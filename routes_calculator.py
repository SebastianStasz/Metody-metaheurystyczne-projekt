from chromosome import get_solution
import time


def city_index_to_city(index, cities):
    return cities[index]


def get_best_routes(cities, number_of_cars, single_car_capacity, number_of_generations):
    start = time.time()
    required_total_cities = len(cities) + 2 * number_of_cars - 1
    total_cities = 0
    
    while total_cities != required_total_cities:
        chromosome = get_solution(cities, number_of_cars, number_of_generations, single_car_capacity)
        total_capacity = 0
        total_cities = 0
        cars_result = []
        
        for i in range(chromosome.m):
            required_capacity = 0
            car_number = i + 1
            route = []
            city_index = chromosome.solution[i][0]
            city = city_index_to_city(city_index, cities)
            route.append(city)
            required_capacity += city['demand']
            
            for j in range(1,len(chromosome.solution[i])):
                city_index = chromosome.solution[i][j]
                city = city_index_to_city(city_index, cities)
                route.append(city)
                required_capacity += city['demand']
            
            car = {"number": car_number, "load": required_capacity, "route": route}
            cars_result.append(car)
            
            if required_capacity > single_car_capacity:
                break
            
            total_cities += len(chromosome.solution[i])
            total_capacity += required_capacity

        end = time.time()
    
    total_distance = round(chromosome.cost, 2)
    return {'cars_result': cars_result,
            'total_distance': total_distance,
            'total_capacity': total_capacity,
            'execution_time': end - start}
