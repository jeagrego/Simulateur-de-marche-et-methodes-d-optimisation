import pymunk.pygame_util

from Animal import *
from DifferentialEvolution import *
from Environment import Environment
from Genetic import *


class Model:

    def __init__(self, mutation_prob, footNumber, weight, w_body, h_body):
        self.space = pymunk.Space()
        self.environment = Environment(self.space)
        self.genetic = Genetic(footNumber)
        self.differential_evolution = DifferentialEvolution([])
        self.population = []
        self.footnumber = footNumber
        self.weight = weight
        self.w_body = w_body
        self.h_body = h_body
        self.mutation_prob = mutation_prob
        self.bestSCore = 0
        self.individu = 0
        self.generation = 0
        self.fallenAnimals = []
        self.distance_final = 0
        self.timer = 0
        self.checkParameters()

    def checkParameters(self):
        if self.footnumber == 4:
            self.initPopulation()
        else:
            raise Exception("Error : wrong feet numbers")

    def getSpace(self):
        return self.space

    def getBestScore(self):
        bestScore = 0
        for individu in self.population:
            score = individu.getScore()
            if individu.getScore() > bestScore:
                bestScore = score
        return bestScore

    def removeFromSpace(self):
        for body in self.space.bodies:
            self.space.remove(body)
        for shape in self.space.shapes:
            self.space.remove(shape)
        for contraint in self.space.constraints:
            self.space.remove(contraint)
        self.environment.setGround()

    def setAnimal(self):
        """
            Ajoute toute la population dans l'environment
        """
        """self.space = pymunk.Space()
        self.environment.setSpace(self.space)"""

        for animal in self.population:
            self.environment.addAnimal(animal)

    def removeAnimal(self, animal):
        for body, shape in animal.getBodyAndShape():
            self.space.remove(body)
            self.space.remove(shape)
        for contraint in animal.getContraints():
            self.space.remove(contraint)

    def getPopulation(self):
        return self.population

    def setPopulation(self, new_population):
        self.population = new_population

    def balanced(self):
        for i in range(int(len(self.population) / 2)):
            self.population.pop(0)

    def deleteAnimal(self, animal):
        self.population.remove(animal)

    def sortPopulation(self):
        animalAndScore = []
        for animal in self.population:
            animalAndScore.append((animal, animal.getScore()))
        animalAndScore = sorted(animalAndScore, key=lambda tup: tup[1])
        self.population = [animal[0] for animal in animalAndScore]
        currentBestScore = self.population[-1].getScore()
        if self.bestSCore < currentBestScore:
            self.bestSCore = self.population[-1].getScore()
            self.writeBest(self.population[-1])

    def writeBest(self, animal):
        score = animal.getScore()
        matrice = animal.getMatrix()

        file1 = open("best_individu.txt", "w")
        file1.write(str(score) + "\n")
        for i in range(self.footnumber * 2):
            line = ""
            for j in range(len(matrice[i])):
                line += str(matrice[i][j]) + " "
            line += "\n"
            file1.write(line)

    def makeNewPopulation(self):
        new_population = self.genetic.get_new_population(self.population, self.mutation_prob)
        self.population = []
        for i in range(len(new_population)):
            animal = Cow(self.footnumber, self.weight,
                         self.w_body, self.h_body)
            animal.setMatrix(new_population[i])
            self.population.append(animal)

    def initPopulation(self):
        for i in range(10):
            animal = self.makeAnimal()
            self.population.append(animal)

    def makeAnimal(self):
        if self.footnumber == 4:
            animal = Cow(self.footnumber, self.weight,
                         self.w_body, self.h_body)
            matrix = self.makeMatrix()
            animal.setMatrix(matrix)
        return animal

    def makeMatrix(self):
        """ Crée une matrice des paramètres utilisés pour faire marcher un animal pour les individus de premiere
        generation. Il y a 6 paramètres.
            Les paramètres de la matrice représentent:
        - L'index de la partie de la jambe à bouger
        - La vitesse moyenne de rotation du genou
        - La direction de la rotation du genou  (jambe arriére axe x)
        - La direction de la rotation de la hanche (jambe arrière axe x)
        - La direction de la rotation du genou  (jambe avant axe x)
        - La direction de la rotation de la hanche (jambe avant axe x)

            :return: la matrice des 6 paramètres initialisés à des valeurs aléatoires pour les jambes au premier plan et
            en arrière plan
            :rtype: list(list(int or float), list(int or float))
        """
        matrix = []
        y = self.footnumber * 2
        for i in range(y):
            x = [random.randint(0, 7), random.uniform(-5.0, 5.0), random.randint(-1, 1), random.randint(-1, 1), random.randint(-1, 1), random.randint(-1, 1)]
            matrix.append(x)
        return matrix

    def moves(self, direction, animal):
        """
            Fait bouger les parties des jambes dependant de la matrice
        """
        topBody = animal.getTopBodyAndHeadBody()[0]
        matrix = animal.getMatrix()
        self.smjoints = animal.getSmjoints()

        direction_1 = [1, -1, -1, -1, -1, -1, -1, 1]  # 1
        direction_2 = [-1, -1, 1, 1, 1, 1, -1, -1]  # 2
        direction_3 = [-1, 1, 1, 1, 1, 1, 1, -1]  # -1
        direction_4 = [1, 1, -1, -1, -1, -1, 1, 1]  # -2

        for k in range(len(self.smjoints)):
            self.smjoints[k].rate = 0

        if direction == 1:
            for i in range(len(matrix)):
                self.smjoints[matrix[i][0]].rate = matrix[i][1] * matrix[i][2]

        elif direction == 2:
            for i in range(len(matrix)):
                self.smjoints[matrix[i][0]].rate = matrix[i][1] * matrix[i][3]

        elif direction == -1:
            for i in range(len(matrix)):
                if i not in [1, 6]:
                    self.smjoints[matrix[i][0]].rate = matrix[i][1] * matrix[i][4]

        elif direction == -2:
            for i in range(len(matrix)):
                self.smjoints[matrix[i][0]].rate = matrix[i][1] * matrix[i][5]

    def getScore(self, i):
        return self.population[i].getScore()

    def getScoreAverage(self):
        avg_score = 0
        for animal in self.population[7:]:
            avg_score += animal.getScore()
        return avg_score

    def completeScoreGeneration(self, generationNumber):
        avg_score = self.getScoreAverage()
        file1 = open("score_generation.txt", "a")
        line = str(generationNumber) + " " + str(avg_score / 3) + "\n"
        file1.write(line)

    def run_simulation(self, direction):
        if self.individu == 0:
            self.individu = 10
            self.i = 0
            self.direction = 1
            if self.generation != 0:
                self.makeNewPopulation()
            self.setAnimal()
            self.fallenAnimals = []
            self.setNewTimer()

        for indexAnimal in range(len(self.population)):
            if indexAnimal not in self.fallenAnimals:
                time_gap = time() - self.timer
                animal = self.population[indexAnimal]
                self.top, self.head = animal.getTopBodyAndHeadBody()
                isMoving = animal.isMoving(time_gap)
                isNotFalling = animal.isNotFalling(time_gap)

                if isMoving and isNotFalling:
                    self.start_time = time()
                    self.moves(direction, animal)
                    # self.distance = self.top.position[0] - animal.getPosition()[0]
                    animal.updateTime()

                else:
                    self.removeAnimal(animal)
                    self.fallenAnimals.append(indexAnimal)

                    if self.individu == 1:
                        self.sortPopulation()
                        self.completeScoreGeneration(self.generation)
                        self.generation += 1
                    self.individu -= 1
                distance = (self.top.position[0] - animal.getInitPos()[0])
                individu_timer = time() - self.timer
                if individu_timer > 0:
                    score = distance + ((1 / individu_timer) * 100)
                    animal.setScore(score)  # TODO revoir le score

        return self.generation, self.individu

    def setNewTimer(self):
        self.timer = time()
