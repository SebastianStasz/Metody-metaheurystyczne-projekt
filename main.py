from results_presenter import print_result
from routes_calculator import get_best_routes
from cities import cities


if __name__ == '__main__':
    number_of_cars = 5
    single_car_capacity = 1000
    
    result = get_best_routes(cities, number_of_cars, single_car_capacity)
    print_result(result)
