import random
import Animal



class Genetic:
    def __init__(self, footNumber):
        self.leg_set = [i for i in range((footNumber*2)-1)]
        self.rotation_set = [random.uniform(-5, 5) for i in range(100)]
        self.population = None
        self.footNumber = footNumber
        #print(self.rotation_set)

    def updatePopulation(self, population):
        self.population = population

    def crossover(self, parent_1, parent_2):
        """
        Crée deux nouveaux individus en combinant les chaînes des parents. Le point de coupure est choisi aléatoirement
        """
        if len(parent_1[0]) <= 1:
            return parent_1
        index = random.randrange(1, len(parent_1[0]))
        
        child_1 = (parent_1[0][:index] + parent_2[0][index:], parent_1[1])
        #child_2 = (parent_2[0][:index] + parent_1[0][index:], parent_2[1]) a essayer
        return child_1

    def mutate(self, individual):
        """
        Modifie une chaîne individuelle en remplaçant aléatoirement un caractère par un autre caractère dans gene_set
        """

        leg_index = random.randrange(0, len(self.leg_set)-1)
        rotation_index = random.randrange(0, len(self.leg_set)-1)

        individual[leg_index][0] = self.leg_set[random.randint(0, len(self.leg_set)-1)]
        individual[rotation_index][1] = self.rotation_set[random.randint(0, len(self.rotation_set)-1)]

        return individual

    def get_random_parents(self, population):
        index = len(population) // 2

        if len(population) == 2:
            return population[0], population[1]

        parent_1 = population[random.randint(0, index)]
        parent_2 = population[-1]
        return parent_1, parent_2


    def get_new_population(self, population, mutation_prob):
        population_2 = []
        population_size = len(population)
        for i in range(population_size):
            parent_1, parent_2 = self.get_random_parents(population)
            child = self.crossover((parent_1.getMatrix(), parent_1.getScore()), (parent_2.getMatrix(), parent_2.getScore()))[0]
            
            if random.uniform(0, 1) <= mutation_prob:
                child = self.mutate(child)

            population_2.append(child)
            if population_size == 1:
                return population_2
        return population_2