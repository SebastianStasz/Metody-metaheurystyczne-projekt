from results_presenter import print_result
from routes_calculator import get_best_routes
from cities import cities


if __name__ == '__main__':
    algorithm_iterations = 10
    single_car_capacity = 1000
    number_of_cars = 5
    
    best_result = None
    
    for i in range(10):
        result = get_best_routes(cities, number_of_cars, single_car_capacity)
        total_distance = result['total_distance']
        print(f'Result {i + 1}:\nTotal distance: {total_distance} km\n')
        
        if best_result == None or best_result['total_distance'] > total_distance:
            best_result = result
    
    print('----------------------------------------\n')
    print_result(best_result)
