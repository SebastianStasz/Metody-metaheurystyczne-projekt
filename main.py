import numpy as np
import copy
from tqdm import tqdm
from cities import cities
from distances import get_distances_between_cities

number_of_cities = len(cities)
number_of_cars = 5


class Chromosome():
    # Random generated Chromosome
    def __init__(self, number_of_cities, number_of_traveling_salesman, adj = get_distances_between_cities(cities)):
        self.n = number_of_cities
        self.m = number_of_traveling_salesman
        self.adj = adj
        c = np.array(range(1,number_of_cities))
        np.random.shuffle(c)
        self.solution = np.array_split(c, self.m)
        for i in range(len(self.solution)):
            self.solution[i] = np.insert(self.solution[i],0,0)
            self.solution[i] = np.append(self.solution[i],0)
        self.fitness()
            

    def fitness(self):
        self.cost = 0
        longest_salesman_fitness = []
        longest_salesman_length = 0
        for i in range(self.m):
            salesman = self.solution[i]
            salesman_fitness = 0
            for j in range(len(salesman) - 1):
                salesman_fitness = salesman_fitness + self.adj[salesman[j]][salesman[j+1]]
            self.cost = self.cost + salesman_fitness
            if len(salesman) > longest_salesman_length or (len(salesman) == longest_salesman_length and salesman_fitness > self.minmax):
                longest_salesman_length = len(salesman)
                self.minmax = salesman_fitness
        self.score = self.cost + self.minmax
    

    def mutate_local(self):
        index = np.random.randint(0,self.m)
        mutant = self.solution[index]
        i,j = np.random.randint(1,len(mutant)-1), np.random.randint(1,len(mutant)-1)
        mutant[i], mutant[j] = mutant[j], mutant[i]
        old_cost = self.cost
        self.fitness()
    

    def mutate_global(self):
        for i in range(self.m):
            if len(self.solution[i]) < 3:
                print(i, self.solution[i])
        
        
        index1, index2 = np.random.randint(0,self.m), np.random.randint(0,self.m)
        while index1 == index2:
            index1, index2 = np.random.randint(0,self.m), np.random.randint(0,self.m)
        while len(self.solution[index1]) < 4:
            index1, index2 = np.random.randint(0,self.m), np.random.randint(0,self.m)
        mutant1, mutant2 = self.solution[index1], self.solution[index2]
        i,j = np.random.randint(1,len(mutant1)-1), np.random.randint(1,len(mutant2)-1)
        self.solution[index2] = np.insert(mutant2, j, mutant1[i])
        self.solution[index1] = np.delete(mutant1, i)
        old_cost = self.cost
        self.fitness()

def get_solution():
    chromosome = Chromosome(number_of_cities = number_of_cities, number_of_traveling_salesman = number_of_cars)
    for it in tqdm(range(100)):
        chromosome_copy = copy.deepcopy(chromosome)
        chromosome_copy.mutate_global()
        if chromosome_copy.score < chromosome.score:
            chromosome = chromosome_copy

        chromosome_copy = copy.deepcopy(chromosome)
        chromosome_copy.mutate_local()
        if chromosome_copy.score < chromosome.score:
            chromosome = chromosome_copy
    
    return chromosome

def city_index_to_city(index):
    return cities[index]


total_cities = 0
while total_cities != 40:
    chromosome = get_solution()
    total_cities = 0
    for i in range(chromosome.m):
        output = ""
        required_capacity = 0
        car_number = i + 1
        city_index = chromosome.solution[i][0]
        city = city_index_to_city(city_index)
        required_capacity += city['demand']
        output += f'Car {car_number}: {city["name"]}'
        for j in range(1,len(chromosome.solution[i])):
            city_index = chromosome.solution[i][j]
            city = city_index_to_city(city_index)
            required_capacity += city['demand']
            output += ' - ' + f'{city["name"]}'
        output += f' --- # {len(chromosome.solution[i])}'
        print(output)
        print(f'Required capacity: {required_capacity}')
        if required_capacity > 1000:
            break
        total_cities += len(chromosome.solution[i])

    print(total_cities)
    print("Total distance: ", chromosome.cost)
