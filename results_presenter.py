import matplotlib.pyplot as plt


def plot_coordinates(data):
    for i, path in enumerate(data):
        x_values = [point['coordinates']['x'] for point in path]
        y_values = [point['coordinates']['y'] for point in path]
        x_values.append(x_values[0])
        y_values.append(y_values[0])
        plt.plot(x_values, y_values, marker='o', label=f'Car {i + 1}')

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Routes')
    plt.legend()
    plt.grid(True)
    plt.show()


def print_result(result):
    cars_result = result['cars_result']
    total_distance = result['total_distance']
    total_capacity = result['total_capacity']
    
    routes = []
    
    for car in cars_result:
        car_number = car['number']
        car_load = car['load']
        car_route = [route for route in car['route']]
        cities = [city['name'] for city in car_route]
        routes.append(car_route)
        
        print(f'Car {car_number}')
        print(f'Load: {car_load}')
        print(' -> '.join(cities))
        print('')

    print('')
    print(f'Total distance: {total_distance} km')
    print(f'Total capacity: {total_capacity} kg')
    
    plot_coordinates(routes)
