import numpy as np

class DifferentialEvolution:
    def __init__(self, population, mut=0.8, cr=0.7, tol=1e-6):
        #instead of obj func use score of each individual of population
        self.population = population
        self.bounds = [np.random.uniform(-5, 5) for i in range(100)]
        self.mut = mut
        self.cr = cr
        self.tol = tol
        self.best_idx = 0

    def updatePopulation(self, population):
        self.population = population

    def optimize(self):
        # Initialize population randomly within the bounds
        pop = np.random.rand(len(self.population), len(self.bounds)) * (self.bounds[:, 1] - self.bounds[:, 0]) + self.bounds[:,0]

        # Create new population by mutation and crossover
        mutant_pop = self.mutate(pop)
        cross_pop = self.crossover(pop, mutant_pop)

        # Evaluate the objective function for the new population
        fitness = np.array([self.population[ind].getScore() for ind in cross_pop]) #self.population(i).getScore()

        # Select the best individuals for the next generation
        idx = np.argsort(fitness)
        pop = cross_pop[idx[:len(self.population)], :]

        # Return the best individual and its fitness
        self.best_idx = np.argmin(fitness)
        best_sol = pop[self.best_idx, :]

        return best_sol

    def mutate(self, pop):
        # Perform mutation by adding a weighted difference between two randomly selected individuals
        idx1 = np.random.randint(0, len(self.population), len(self.population))
        idx2 = np.random.randint(0, len(self.population), len(self.population))
        mutant_pop = pop + self.mut * (pop[idx1, :] - pop[idx2, :])
        mutant_pop = np.clip(mutant_pop, self.bounds[:, 0], self.bounds[:, 1])
        return mutant_pop

    def crossover(self, pop, mutant_pop):
        # Perform crossover by selecting random elements from the mutant population with a probability of cr
        cross_pop = np.zeros_like(pop)
        for i in range(len(self.population)):
            j_rand = np.random.randint(0, len(self.bounds))
            for j in range(len(self.bounds)):
                if np.random.rand() < self.cr or j == j_rand:
                    cross_pop[i, j] = mutant_pop[i, j]
                else:
                    cross_pop[i, j] = pop[i, j]
        cross_pop = np.clip(cross_pop, self.bounds[:, 0], self.bounds[:, 1])
        return cross_pop

