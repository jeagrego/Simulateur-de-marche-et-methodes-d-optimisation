import random


class Genetic:
    def __init__(self, foot_number):
        self.leg_set = [i for i in range((foot_number * 2) - 1)]
        self.rotation_set = [random.uniform(-5, 5) for i in range(100)]
        self.footNumber = foot_number

    def crossover(self, matrice_p1, matrice_p2):
        """Crée un nouvel individu en combinant les génes des parents. Le génome est représenté ici par une matrice.
        La combinaison des genes, pour un gene donné, prend une valeure aléatoire dans l'intervalle réel des 2 parents.

        :param matrice_p1: La liste la matrice des parametres du parent 2.
        :type matrice_p1: list

        :param matrice_p2: La liste la matrice des parametres du parent 2.
        :type matrice_p2: list

        :return: La liste de la matrice du nouvel animal créé à partir des deux parents.
        :rtype: list
        """
        num_params = len(matrice_p1)
        if num_params <= 1:
            return matrice_p1
        # index = random.randrange(1, len(matrice_p1))
        child = []  # The child parameters become the parameter matrix
        for i in range(num_params):
            params_c = []  # The child parameters used to create the matrix
            leg_index = random.choice([matrice_p1[i][0], matrice_p2[i][0]])
            average_rotation = (matrice_p1[i][1] + matrice_p2[i][1]) / 2
            rotation_direction_1 = random.choice([matrice_p1[i][2], matrice_p2[i][2]])
            rotation_direction_2 = random.choice([matrice_p1[i][3], matrice_p2[i][3]])
            rotation_direction_3 = random.choice([matrice_p1[i][4], matrice_p2[i][4]])
            rotation_direction_4 = random.choice([matrice_p1[i][5], matrice_p2[i][5]])
            params_c.append(leg_index)
            params_c.append(average_rotation)
            params_c.append(rotation_direction_1)
            params_c.append(rotation_direction_2)
            params_c.append(rotation_direction_3)
            params_c.append(rotation_direction_4)
            child.append(params_c)
        # child = (matrice_p1[:index] + matrice_p2[index:], score_p1)
        print(child)
        return child

    def mutate(self, individual):
        """
        Modifie une chaîne individuelle en remplaçant aléatoirement un caractère par un autre caractère dans gene_set
        """

        rotation_index_1 = random.randrange(0, len(self.leg_set) - 1)
        # rotation_index_2 = random.randrange(0, len(self.leg_set) - 1)

        individual[rotation_index_1][1] = self.rotation_set[random.randint(0, len(self.rotation_set) - 1)]
        # individual[rotation_index_2][1] = self.rotation_set[random.randint(0, len(self.rotation_set) - 1)]

        return individual

    # def get_random_parents(self, population):
    # index = len(population) // 2

    # if len(population) == 2:
    # return population[0], population[1]

    # parent1 = population[random.randint(0, index)]
    # parent2 = population[-1]

    # return parent1, parent2

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
                parent1 = indiv
                break

        # répéter les étapes 2 à 4 pour sélectionner le deuxième parent
        random_num = random.uniform(0, total_score)
        cum_score = 0
        for indiv in population:
            cum_score += indiv.getScore()
            if cum_score >= random_num:
                parent2 = indiv
                break

        return parent1, parent2

    def get_new_population(self, population, mutation_prob):
        population_2 = []
        population_size = len(population)
        for i in range(population_size):
            parent1, parent2 = self.get_not_random_parents(population)  # changed to get_random_parent
            child = self.crossover(parent1.getMatrix(), parent2.getMatrix())

            if random.uniform(0, 1) <= mutation_prob:
                child = self.mutate(child)

            population_2.append(child)
            if population_size == 1:
                return population_2
        return population_2
