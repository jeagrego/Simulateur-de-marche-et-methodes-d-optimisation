import pymunk
import pymunk.pygame_util
from Environment import Environment
from Animal import *
from Genetic import *
import time


class Model:

    def __init__(self, mutation_prob, footNumber, weight, w_body, h_body, x_animal=150, y_animal=332.75):
        self.space = pymunk.Space()
        self.environment = Environment(self.space)
        self.genetic = Genetic(footNumber)
        self.population = []
        self.footnumber = footNumber
        self.weight = weight
        self.w_body = w_body
        self.h_body = h_body
        self.x_animal = x_animal
        self.y_animal = y_animal
        self.x_previous_body = x_animal
        self.y_previous_body = y_animal
        self.mutation_prob = mutation_prob
        self.time = 0
        self.diff_x = 0
        self.interval_time = 0

        if footNumber == 4:
            self.initPopulation()
    
        elif footNumber == 2:
            print("unavailable")

        else:
            raise Exception("Error : wrong foot numbers")

    def getSpace(self):
        return self.space

    def getPosition(self):
        return (self.x_animal, self.y_animal)

    def setAnimal(self, animal, time):
        """
            Supprime tous les bodies and shapes dans le parametre space. Et set l'animal et le sol
        """
        self.interval_time = time
        for body in self.space.bodies:
            self.space.remove(body)
        for shape in self.space.shapes:
            self.space.remove(shape)
        for constraint in self.space.constraints:
            self.space.remove(constraint)
        self.environment.setGround()
        self.environment.addAnimal(animal)
        self.x_previous_body = self.x_animal
        self.y_previous_body = self.y_animal

    def getPopulation(self):
        return self.population

    def addToPopulation(self, new_population):
        self.population.extend(new_population)
        self.sortPopulation()
    
    def deleteAnimal(self, animal):
        self.population.remove(animal)

    def sortPopulation(self):
        animalAndScore = []
        for animal in self.population:
            animalAndScore.append((animal, animal.getScore()))
        
        animalAndScore = sorted(animalAndScore, key=lambda tup: tup[1])
        print(animalAndScore)
        self.population = [animal[0] for animal in animalAndScore]

    def getNewPopulation(self):
        new_population = self.genetic.get_new_population(self.population, self.mutation_prob)
        new_population_1 = []
        for i in range(len(new_population)):
            animal = self.makeAnimal()
            animal.setMatrix(new_population[i])
            new_population_1.append(animal)
        return new_population_1

    def isMoving(self):
        if self.time // 5 == 1:
            self.time = 0
            self.interval_time = time.time()
            if abs(self.diff_x) < 100:
                self.diff_x = 0
                self.time = 0
                return False
        return True

    def isNotFalling(self, headBody):
        diff_y = self.y_animal - headBody.position[1]
        if abs(diff_y) > self.w_body*0.5:
            return False
        return True

    def initPopulation(self):
        for i in range(2):
            animal = self.makeAnimal()
            self.population.append(animal)    
        self.genetic.updatePopulation(self.population)

    def makeAnimal(self):
        """
            Crée les 2 premiers parents
        """
        if self.footnumber == 4:
            animal = Cow(self.footnumber, self.weight, 
                        self.w_body, self.h_body, 
                        self.x_animal, self.y_animal)
            animal.setMatrix(self.makeMatrix())
        elif self.footnumber == 2:
            animal = Autruche(self.footnumber, self.weight, 
                            self.w_body, self.h_body, 
                            self.x_animal, self.y_animal)
            animal.setMatrix(self.makeMatrix())
        
        return animal

    def makeMatrix(self):
        """
            Crée une matrice pour les 2 premiers parents
        """
        matrix = []
        y = self.footnumber*2
        for i in range(y):
            x = [random.randint(0,y-1), random.uniform(-5.0, 5.0)]
            matrix.append(x)
        return matrix

    def moves(self, direction, animal):
        """
            Fait bouger les parties des jambes dependant de la matrice
        """
        self.time += time.time() - self.interval_time
        topBody = animal.getTopBodyAndHeadBody()[0]
        self.diff_x += self.x_previous_body - topBody.position[0]
        self.x_previous_body = topBody.position[0]
        matrix = animal.getMatrix()
        self.smjoints = animal.getSmjoints()

        direction_1 = [1, -1 , -1, -1 , -1, -1 , -1, 1] #1
        direction_2 = [-1, -1, 1 ,1 ,1 ,1, -1, -1] #2
        direction_3 = [-1, 1, 1 ,1 ,1 ,1, 1, -1] #-1
        direction_4 = [1, 1 , -1, -1 , -1, -1 , 1, 1] #-2

        for k in range(len(self.smjoints)):
            self.smjoints[k].rate = 0
        
        if direction == 1:
            for i in range(len(matrix)):
                if i not in [1, 6]:
                    self.smjoints[matrix[i][0]].rate = matrix[i][1]*direction_1[i]
            
        elif direction == 2:
            for i in range(len(matrix)):
                self.smjoints[matrix[i][0]].rate = matrix[i][1]*direction_2[i]

        elif direction == -1:
            for i in range(len(matrix)):
                if i not in [1, 6]:
                    self.smjoints[matrix[i][0]].rate = matrix[i][1]*direction_3[i]
            
        elif direction == -2:
            for i in range(len(matrix)):
                self.smjoints[matrix[i][0]].rate = matrix[i][1]*direction_4[i]
        
    