import copy
import numpy as np
from distances_calculator import get_distances_between_cities
from simulated_annealing import SimulatedAnnealing


class Problem:
    def __init__(self, cities, number_of_cars, single_car_capacity):
        self.single_car_capacity = single_car_capacity
        self.n = len(cities)
        self.m = number_of_cars
        self.adj = get_distances_between_cities(cities)
        self.cities = cities

        c = np.array(range(1, self.n))
        np.random.shuffle(c)
        self.solution = np.array_split(c, self.m)
        for i in range(len(self.solution)):
            self.solution[i] = np.insert(self.solution[i], 0, 0)
            self.solution[i] = np.append(self.solution[i], 0)

    def get_solution(self):
        return copy.deepcopy(self.solution)

    def cost(self, solution=None):
        if solution is None:
            solution = self.solution
        cost = 0
        for i in range(self.m):
            salesman = solution[i]
            salesman_cost = 0
            for j in range(len(salesman) - 1):
                salesman_cost += self.adj[salesman[j]][salesman[j + 1]]
            cost += salesman_cost
        return cost

    def random_move(self):
        new_solution = self.get_solution()
        self.mutate_local(new_solution)
        self.mutate_global(new_solution)
        new_cost = self.cost(new_solution)
        return new_cost, new_solution

    def make_move(self, new_solution):
        self.solution = new_solution

    def mutate_local(self, solution):
        index = np.random.randint(0, self.m)
        mutant = solution[index]
        i, j = np.random.randint(1, len(mutant) - 1), np.random.randint(1, len(mutant) - 1)
        mutant[i], mutant[j] = mutant[j], mutant[i]

    def mutate_global(self, solution):
        index1, index2 = self.get_random_cars()
        mutant1, mutant2 = solution[index1], solution[index2]
        i, j = np.random.randint(1, len(mutant1) - 1), np.random.randint(1, len(mutant2) - 1)
        sample_solution = np.insert(mutant2, j, mutant1[i])

        while self.get_total_load(sample_solution) > self.single_car_capacity:
            index1, index2 = self.get_random_cars()
            mutant1, mutant2 = solution[index1], solution[index2]
            i, j = np.random.randint(1, len(mutant1) - 1), np.random.randint(1, len(mutant2) - 1)
            sample_solution = np.insert(mutant2, j, mutant1[i])

        solution[index2] = np.insert(mutant2, j, mutant1[i])
        solution[index1] = np.delete(mutant1, i)

    def get_total_load(self, route):
        cities = [self.cities[city_id] for city_id in route]
        return sum([city["demand"] for city in cities])

    def get_random_cars(self):
        index1, index2 = np.random.randint(0, self.m), np.random.randint(0, self.m)
        while index1 == index2:
            index1, index2 = np.random.randint(0, self.m), np.random.randint(0, self.m)
        return index1, index2


def get_solution(cities, number_of_cars, single_car_capacity, T, T_min, n, alfa):
    problem = Problem(cities, number_of_cars, single_car_capacity)
    sa = SimulatedAnnealing(problem, T=T, T_min=T_min, n=n, alfa=alfa)
    sa.optimize()
    return sa.best_state, sa.min_cost, sa.temperatures, sa.costs
