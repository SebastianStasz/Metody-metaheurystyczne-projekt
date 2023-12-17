from results_presenter import print_result
from routes_calculator import get_best_routes
from cities import cities


def find_solution(algorithm_iterations, number_of_cars, population_size, number_of_generations, single_car_capacity):
    best_result = None

    for i in range(algorithm_iterations):
        result = get_best_routes(cities, number_of_cars, population_size, number_of_generations, single_car_capacity)
        total_distance = result['total_distance']
        print(f'Result {i + 1}:\nTotal distance: {total_distance} km.')
        print(f'Execution time: {round(result["execution_time"], 2)} seconds.\n')

        if best_result is None or best_result['total_distance'] > total_distance:
            best_result = result

    print('----------------------------------------')
    print('Best solution')
    print(f'Execution time: {round(result["execution_time"], 2)} seconds.\n')
    print_result(best_result)


def main():
    algorithm_iterations = 1
    population_size = 20
    number_of_generations = 100
    single_car_capacity = 1000
    number_of_cars = 5

    required_capacity = sum([city['demand'] for city in cities])
    available_capacity = number_of_cars * single_car_capacity

    print(f'Required capacity: {required_capacity} kg')
    print(f'Available capacity: {available_capacity} kg')

    if required_capacity > available_capacity:
        print('No possible solution. The available capacity is not sufficient.')
    else:
        print('Solution is possible. Calculating...\n')
        find_solution(algorithm_iterations, number_of_cars, population_size, number_of_generations, single_car_capacity)


if __name__ == '__main__':
    main()
