import random
import Animal



class Genetic:
    def __init__(self, footNumber):
        self.leg_set = [i for i in range((footNumber*2)-1)]
        self.rotation_set = [random.uniform(-5, 5) for i in range(100)]
        self.footNumber = footNumber

    def crossover(self, parent_1, parent_2):
        """
        Crée deux nouveaux individus en combinant les chaînes des parents. Le point de coupure est choisi aléatoirement
        """
        if len(parent_1[0]) <= 1:
            return parent_1
        index = random.randrange(1, len(parent_1[0]))
        child_1 = ([],0)
        for i in range(len(parent_1[0])):
            moyen = (parent_1[0][i][1] + parent_2[0][i][1])/2
            line = []
            line.append(i)
            line.append(moyen)
            child_1[0].append(line)
        #child_1 = (parent_1[0][:index] + parent_2[0][index:], parent_1[1])
        """print("parent 1 :")
        print(parent_1)
        print("parent 2 :")
        print(parent_2)
        print("child 1 :")
        print(child_1)"""
        return child_1

    def mutate(self, individual):
        """
        Modifie une chaîne individuelle en remplaçant aléatoirement un caractère par un autre caractère dans gene_set
        """

        rotation_index_1 = random.randrange(0, len(self.leg_set)-1)
        rotation_index_2 = random.randrange(0, len(self.leg_set)-1)

        individual[rotation_index_1][1] = self.rotation_set[random.randint(0, len(self.rotation_set)-1)]
        individual[rotation_index_2][1] = self.rotation_set[random.randint(0, len(self.rotation_set)-1)]

        return individual

    def get_random_parents(self, population):
        index = len(population) // 2

        if len(population) == 2:
            return population[0], population[1]

        parent_1 = population[random.randint(0, index)]
        parent_2 = population[-1]
        """print("random parent 1 :")
        print(parent_1)
        print("random parent 2 :")
        print(parent_2)"""
        return parent_1, parent_2

    def get_not_random_parents(self, population):
        # calculer la somme totale des scores
        total_score = sum([indiv.getScore() for indiv in population])

        # sélectionner un nombre aléatoire entre 0 et la somme totale des scores
        random_num = random.uniform(0, total_score)

        # sélectionner le premier parent
        cum_score = 0
        for indiv in population:
            cum_score += indiv.getScore()
            if cum_score >= random_num:
                parent_1 = indiv
                break

        # répéter les étapes 2 à 4 pour sélectionner le deuxième parent
        random_num = random.uniform(0, total_score)
        cum_score = 0
        for indiv in population:
            cum_score += indiv.getScore()
            if cum_score >= random_num:
                parent_2 = indiv
                break

        return parent_1, parent_2


    def get_new_population(self, population, mutation_prob):
        population_2 = []
        population_size = len(population)
        for i in range(population_size):
            parent_1, parent_2 = self.get_random_parents(population) #changed to get_random_parent
            child = self.crossover((parent_1.getMatrix(), parent_1.getScore()), (parent_2.getMatrix(), parent_2.getScore()))[0]
            
            if random.uniform(0, 1) <= mutation_prob:
                child = self.mutate(child)

            population_2.append(child)
            if population_size == 1:
                return population_2
        return population_2