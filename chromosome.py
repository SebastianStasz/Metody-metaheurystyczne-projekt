import numpy as np
from distances_calculator import get_distances_between_cities
from math import inf


class Chromosome:
    def __init__(self, number_of_cities, number_of_cars, single_car_capacity, cities, solution=None):
        self.single_car_capacity = single_car_capacity
        self.n = number_of_cities
        self.m = number_of_cars
        self.adj = get_distances_between_cities(cities)
        self.cities = cities
        self.cost = 0
        self.score = 0
        self.minmax = 0
        self.solution = solution

        if self.solution is None:
            c = np.array(range(1, number_of_cities))
            np.random.shuffle(c)
            self.solution = np.array_split(c, self.m)

            for i in range(len(self.solution)):
                self.solution[i] = np.insert(self.solution[i], 0, 0)
                self.solution[i] = np.append(self.solution[i], 0)

        self.fitness()

    def fitness(self):
        self.cost = 0
        longest_salesman_length = 0
        for i in range(self.m):
            salesman = self.solution[i]
            salesman_fitness = 0
            for j in range(len(salesman) - 1):
                salesman_fitness = salesman_fitness + self.adj[salesman[j]][salesman[j + 1]]
            self.cost = self.cost + salesman_fitness
            if len(salesman) > longest_salesman_length or (
                    len(salesman) == longest_salesman_length and salesman_fitness > self.minmax):
                longest_salesman_length = len(salesman)
                self.minmax = salesman_fitness
        self.score = self.cost + self.minmax

    def mutate_local(self):
        index = np.random.randint(0, self.m)
        mutant = self.solution[index]
        i, j = np.random.randint(1, len(mutant) - 1), np.random.randint(1, len(mutant) - 1)
        mutant[i], mutant[j] = mutant[j], mutant[i]
        self.fitness()

    def mutate_global(self):
        index1, index2 = self.get_random_cars()
        mutant1, mutant2 = self.solution[index1], self.solution[index2]
        i, j = np.random.randint(1, len(mutant1) - 1), np.random.randint(1, len(mutant2) - 1)
        sample_solution = np.insert(mutant2, j, mutant1[i])

        while self.get_total_load(sample_solution) > self.single_car_capacity:
            index1, index2 = self.get_random_cars()
            mutant1, mutant2 = self.solution[index1], self.solution[index2]
            i, j = np.random.randint(1, len(mutant1) - 1), np.random.randint(1, len(mutant2) - 1)
            sample_solution = np.insert(mutant2, j, mutant1[i])

        self.solution[index2] = np.insert(mutant2, j, mutant1[i])
        self.solution[index1] = np.delete(mutant1, i)
        self.fitness()

    def get_total_load(self, route):
        cities = [self.cities[city_id] for city_id in route]
        return sum([city["demand"] for city in cities])

    def get_random_cars(self):
        index1, index2 = np.random.randint(0, self.m), np.random.randint(0, self.m)
        while index1 == index2:
            index1, index2 = np.random.randint(0, self.m), np.random.randint(0, self.m)
        return index1, index2


def cross_solutions2(chromosome1: Chromosome, chromosome2: Chromosome):
    paths = []
    for i in range(5):
        paths.append(chromosome1.solution[i])
        paths.append(chromosome2.solution[i])

    new_solution = []
    new_solution_cities_set = set()

    for path in paths:
        path_set = set(path) - {0}
        if len(set.intersection(path_set, new_solution_cities_set)) == 0:
            new_solution_cities_set.update(path_set)
            new_solution.append(path)

    if len(new_solution) == 5:
        if np.all([np.array_equal(a, b) for a, b in zip(chromosome1.solution, new_solution)]):
            new_solution = chromosome1.solution
    elif len(new_solution) == 4:
        missing_cities_set = set(range(1, chromosome1.n)) - new_solution_cities_set
        if len(missing_cities_set) < 7:
            missing_cities = np.array(list(missing_cities_set))
            np.random.shuffle(missing_cities)
            np.insert(missing_cities, [0, len(missing_cities)], 0)
            new_solution.append(missing_cities)
        else:
            new_solution = chromosome1.solution
    else:
        new_solution = chromosome1.solution

    return Chromosome(
        number_of_cities=chromosome1.n,
        number_of_cars=chromosome1.m,
        single_car_capacity=chromosome1.single_car_capacity,
        cities=chromosome1.cities,
        solution=new_solution
    )


def get_solution(cities, number_of_cars, population_size, number_of_generations, single_car_capacity):
    number_of_cities = len(cities)

    print("Generating new population...")

    population = np.array(
        [
            Chromosome(
                number_of_cities=number_of_cities,
                number_of_cars=number_of_cars,
                single_car_capacity=single_car_capacity,
                cities=cities
            )
            for _ in range(population_size)
        ]
    )

    half_population = population_size // 2

    for it in range(number_of_generations):
        print("Generation: ", it)

        for chromosome in population[half_population:]:
            chromosome.mutate_global()
            chromosome.mutate_local()

        sorted_scores = np.argsort([chromosome.score for chromosome in population])
        population = population[sorted_scores]
        better_half = population[:half_population]

        population_copy = np.copy(population)
        np.random.shuffle(population_copy)
        random_half = population_copy[half_population:]

        children = np.array(
            [
                cross_solutions2(chromosome1, chromosome2)
                for chromosome1, chromosome2 in zip(random_half, better_half)
            ]
        )

        population = np.concatenate((better_half, children), axis=None)
        print([x.score for x in population])

    best_score = inf
    best_chromosome = None
    for chromosome in population:
        if chromosome.score < best_score:
            best_score = chromosome.score
            best_chromosome = chromosome

    return best_chromosome
