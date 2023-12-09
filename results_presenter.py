import matplotlib.pyplot as plt


def plot_coordinates(data):
    fig, ax = plt.subplots()

    for i, route in enumerate(data):
        city_names = [city['name'] for city in route]
        y = [city['coordinates']['x'] for city in route]
        x = [city['coordinates']['y'] for city in route]
        
        plt.plot(x, y, marker='o', label=f'Car {i + 1}')
        
        for i, name in enumerate(city_names):
            ax.text(x[i], y[i], name)

    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_title('Routes')
    ax.legend()
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
