import pymunk.pygame_util

from walking_sim.Animal import *
from Algorithms.DifferentialEvolution import *
from walking_sim.Environment import Environment
from Algorithms.Genetic import *
from Algorithms.WalterAlgo import *


class Model:

    def __init__(self, mutation_prob, footNumber, weight, w_body, h_body):
        self.space = pymunk.Space()
        self.environment = Environment(self.space)
        self.algo = WalterAlgo(footNumber)#Genetic(footNumber)
        #self.differential_evolution = DifferentialEvolution([])
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
        for contraint in animal.getConstraints():
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

        file1 = open("../txt/best_individu.txt", "w")
        file1.write(str(score) + "\n")
        for i in range(len(matrice)):
            line = ""
            line += str(matrice[i]) + " "
            line += "\n"
            file1.write(line)

    def makeNewPopulation(self):
        new_population = self.algo.get_new_population(self.population, self.mutation_prob)
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
            Les lignes de la matrice représentent:
        H: hanche G: genou B: background F: foreground A: arriere V: avant
        - 0: (HBA) La hanche de la jambe arrière en arrière plan
        - 1: (GBA) Le genou de la jambe arrière en arrière plan
        - 2: (HFA) La hanche de la jambe arrière en premier plan
        - 3: (GFA) Le genou de la jambe arrière en premier plan
        - 4: (HBV) La hanche de la jambe avant en arrière plan
        - 5: (GBV) Le genou de la jambe avant en arrière plan
        - 6: (HFV) La hanche de la jambe avant en premier plan
        - 7: (GFV) Le genou de la jambe avant en premier plan
            Les paramètres de la matrice représentent:
        - La vitesse de rotation du RotationJoint représentant une articulation
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
            matrix.append(random.uniform(0, 3.0))
        return matrix

    def moves(self, direction, animal):
        """
            Fait bouger les parties des jambes en fonction des paramètres de la matrice
        """
        topBody = animal.getTopBodyAndHeadBody()[0]
        matrix = animal.getMatrix()
        self.smjoints = animal.getSmjoints()
        i_direction = 0
        if direction == 1:
            i_direction = 0
        if direction == -1:
            i_direction = 1
        directions = [[1, -1, -1, 0, -1, 0, 1, -1]  # 1
            , [-1, 0, 1, -1, 1, -1, -1, 0]]  # -1

        for k in range(len(self.smjoints)):
            self.smjoints[k].rate = 0
        for i in range(len(matrix)):
            self.smjoints[i].rate = matrix[i] * directions[i_direction][i]

    def getScore(self, i):
        return self.population[i].getScore()

    def getScoreAverage(self):
        avg_score = 0
        for animal in self.population[7:]:
            avg_score += animal.getScore()
        return avg_score

    def completeScoreGeneration(self, generationNumber):
        avg_score = self.getScoreAverage()
        file1 = open("../txt/score_generation.txt", "a")
        line = str(generationNumber) + " " + str(avg_score / 3) + "\n"
        file1.write(line)

    def run_simulation(self, direction):
        if self.individu == 0:
            self.individu = 10
            direction = 1
            if self.generation != 0:
                self.makeNewPopulation()
            self.setAnimal()
            self.fallenAnimals = []
            self.reset_timer()

        for indexAnimal in range(len(self.population)):
            if indexAnimal not in self.fallenAnimals:
                time_gap = time() - self.timer
                animal = self.population[indexAnimal]
                top, head = animal.getTopBodyAndHeadBody()
                is_moving = animal.isMoving(time_gap)
                is_not_falling = animal.isNotFalling(time_gap)

                if is_moving and is_not_falling:
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
                distance = (top.position[0] - animal.getInitPos()[0])
                individu_timer = time() - self.timer
                if individu_timer > 0:
                    score = distance
                    animal.setScore(score)  # TODO revoir le score

        return self.generation, self.individu

    def reset_timer(self):
        self.timer = time()
