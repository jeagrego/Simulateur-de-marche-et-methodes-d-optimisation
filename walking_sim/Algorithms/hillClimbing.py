import random


class Hill_climbing:
    def __init__(self, foot_number):
        self.leg_set = [i for i in range((foot_number * 2) - 1)]
        self.rotation_set = [random.uniform(-4, 4) for i in range(100)]
        self.footNumber = foot_number

    def randomize(self, matrix_p1, random_factor):
        """Crée un nouvel individu en combinant les génes des parents. Le génome est représenté ici par une matrice.
        La combinaison des genes, pour un gene donné, prend une valeure aléatoire dans l'intervalle réel des 2 parents.

        :param matrix_p1: La liste la matrice des parametres du parent 2.
        :type matrix_p1: list

        :param random_factor: un facteur allant de 0 à 1 utilisé pour avoir des enfants plus ou moins similaires au
        parent
        :type random_factor: float

        :return: La liste de la matrice du nouvel animal créé à partir des deux parents.
        :rtype: list
        """
        num_params = len(matrix_p1)
        if num_params <= 1:
            return matrix_p1
        child = []  # The child parameters become the parameter matrix
        for leg_index in range(num_params):
            average_rotation = matrix_p1[leg_index] + random.uniform(-1, 1) * random_factor
            average_rotation = min(max(average_rotation, -5), 5)
            child.append(average_rotation)
        return child

    def get_best_parent(self, population):
        return population[-1]

    def get_new_population(self, population, random_factor):
        population_2 = []
        population_size = len(population)
        random_factor = random_factor / 100
        random_factor_current = random_factor
        parent1 = self.get_best_parent(population)  # changed to get_random_parent
        for i in range(population_size):
            child = self.randomize(parent1.getMatrix(), random_factor_current)  # random_factor_current

            population_2.append(child)
            if population_size == 1:
                return population_2
            else:
                random_factor_current = random_factor_current - (random_factor / (population_size - 1))
        return population_2
