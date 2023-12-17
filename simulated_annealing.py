import numpy as np


class SimulatedAnnealing:
    def __init__(self, problem, T=500, T_min=1, n=500, alfa=0.99):
        self.problem = problem
        self.T_0 = T
        self.T = T
        self.n = n
        self.alfa = alfa

        self.old_cost = self.problem.cost()
        self.T_min = T_min
        self.min_cost = np.inf
        self.best_state = self.problem.get_solution()
        self.costs = []
        self.temperatures = []

    def P(self, new_cost):
        return 1 if new_cost <= self.old_cost else np.exp((self.old_cost - new_cost) / self.T)

    def optimize(self):
        while self.T > self.T_min:
            print("T: ", self.T, " COST:", self.old_cost)

            for _ in range(self.n):
                new_cost, mv = self.problem.random_move()

                if np.random.random() < self.P(new_cost):
                    self.problem.make_move(mv)
                    self.old_cost = new_cost
                    if new_cost < self.min_cost:
                        self.min_cost = new_cost
                        self.best_state = self.problem.get_solution()

            self.costs.append(self.old_cost)
            self.temperatures.append(self.T)
            self.T = self.alfa * self.T
