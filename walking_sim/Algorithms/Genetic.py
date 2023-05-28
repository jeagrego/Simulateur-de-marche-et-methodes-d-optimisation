import random


class Genetic:
    def __init__(self, foot_number):
        self.leg_set = [i for i in range((foot_number * 2) - 1)]
        self.rotation_set = [random.uniform(-4, 4) for i in range(100)]
        self.footNumber = foot_number

    def crossover(self, matrix_p1, matrix_p2):
        """Crée un nouvel individu en combinant les génes des parents. Le génome est représenté ici par une matrice.
        La combinaison des genes, pour un gene donné, prend une valeure aléatoire dans l'intervalle réel des 2 parents.

        :param matrix_p1: La liste la matrice des parametres du parent 2.
        :type matrix_p1: list

        :param matrix_p2: La liste la matrice des parametres du parent 2.
        :type matrix_p2: list

        :return: La liste de la matrice du nouvel animal créé à partir des deux parents.
        :rtype: list
        """
        num_params = len(matrix_p1)
        if num_params <= 1:
            return matrix_p1
        child = []  # The child parameters become the parameter matrix
        
        for leg_index in range(num_params):
            params_c = []  # The child parameters used to create the matrix
            # leg_index = random.choice([matrice_p1[i][0], matrice_p2[i][0]])
            # average_rotation = random.choice([matrix_p1[leg_index], matrix_p2[leg_index]])
            diff_speed_m1_m2 = (matrix_p1[leg_index] - matrix_p2[leg_index]) / 2
            average_rotation = random.uniform(-diff_speed_m1_m2, diff_speed_m1_m2) + (
                        matrix_p1[leg_index] + matrix_p2[leg_index]) / 2
            average_rotation = min(max(average_rotation, -5), 5)
            # params_c.append(average_rotation)
            child.append(average_rotation)
        # child = (matrice_p1[:index] + matrice_p2[index:], score_p1)
        return child

    def mutate(self, individual):
        """
        Modifie une chaîne individuelle en remplaçant aléatoirement un caractère par un autre caractère dans gene_set
        """

        i_leg_part = random.randrange(0, len(self.leg_set) - 1)
        individual[i_leg_part] = self.rotation_set[random.randint(0, len(self.rotation_set) - 1)]
        return individual

    def get_random_parents(self, population):
        index = len(population) // 2

        parent1 = population[random.randint(0, index - 1)]
        parent2 = population[-1]

        return parent1, parent2

    def get_not_random_parents(self, population):
        # calculer la somme totale des scores
        total_score = sum([indiv.getScore() for indiv in population])

        # sélectionner un nombre aléatoire entre 0 et la somme totale des scores
        random_num = random.uniform(0, total_score)

        # sélectionner le premier parent
        cum_score = 0
        parent1 = None
        for indiv in population:
            cum_score += indiv.getScore()
            if cum_score >= random_num:
                parent1 = indiv
                break

        # répéter les étapes 2 à 4 pour sélectionner le deuxième parent
        random_num = random.uniform(0, total_score - parent1.getScore())
        cum_score = 0
        parent2 = None
        for indiv in population:
            if indiv != parent1:
                cum_score += indiv.getScore()
                if cum_score >= random_num:
                    parent2 = indiv
                    break

        return parent1, parent2

    def get_best_parents(self, population):
        print(population[-1].getScore(), population[-2].getScore())
        return population[-1], population[-2]

    def get_new_population(self, population, mutation_prob):
        population_2 = []
        population_size = len(population)
        mutation_prob = mutation_prob / 100
        parent1, parent2 = self.get_not_random_parents(population)  # changed to get_random_parent
        for i in range(population_size):
            child = self.crossover(parent1.getMatrix(), parent2.getMatrix())
            if random.uniform(0, 1) <= mutation_prob:
                child = self.mutate(child)
            population_2.append(child)

        return population_2
