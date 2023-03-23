import pymunk
import pygame
import sys
import pymunk.pygame_util
import Environment
from time import *
from copy import *
from constantes import *
import threading


class Display:

    def __init__(self, model):
        pygame.init()
        self.model = model
        self.space = model.getSpace()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("Arial", 16)
        self.fps = 60
        self.dt = 1.0 / self.fps
        self.individu = 0
        self.generation = 0
        self.new_population = []
        self.fallenAnimals = []
        self.translation = pymunk.Transform()
        self.i = 0
        self.direction = 1  
        self.distance = 0 
        pygame.display.set_caption("Simulation de marche")
        self.translate_speed = 1000
        self.top = pymunk.Body()

    def setDirection(self):
        if self.i == 2:
            self.direction = 2
        if self.i  == 4:
            self.direction = -1
        if self.i  == 6:
            self.direction = -2
        if self.i >= 8:
            self.i = 0
            self.direction = 1  

    def show(self):
        draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        contractMusclesRight = pygame.USEREVENT + 1
        timeToMove = 500
        pygame.time.set_timer(contractMusclesRight, timeToMove, 160000000)
        back_button = pygame.image.load("./imgs/back_arrow.png").convert_alpha()
        back_button_active = pygame.image.load("./imgs/back_arrow_active.png").convert_alpha()
        finish_line = pygame.image.load("./imgs/finish_line.png").convert_alpha()
        grass = pygame.image.load("./imgs/grass1.png").convert_alpha()
        sky = pygame.image.load("./imgs/sky.jpg").convert_alpha()
        x = 50
        y = 50
        while self.running:
            self.setDirection()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 
                elif event.type == contractMusclesRight:
                    self.display_simulation()
                    self.distance = 0
                    self.i += 2

            self.screen.fill(pygame.Color("white"))
            self.screen.blit(sky, (0, 0))
            self.screen.blit(finish_line, (1700, 350))
            #back button
            self.screen.blit(back_button, (x, y))
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if x + 80 > mouse[0] > x and y + 70 > mouse[1] > y:
                if click[0] == 1:
                    return
                self.screen.blit(back_button_active, (x, y))
            #end back button
            self.space.debug_draw(draw_options)
            # Info and flip screen
            self.screen.blit(self.font.render("generation :" + str(self.generation) + " individu: " + str(self.individu) + " Score: " + str(self.distance)
                                              , True, pygame.Color("black")), (0, 0))
            self.screen.blit(grass, (0, 560))
            pygame.display.flip()
            self.space.step(self.dt)
            self.clock.tick(self.fps)
           
    def display_simulation(self):
        if self.individu == 0:
            self.individu = 10
            self.i = 0
            self.direction = 1  
            if self.generation != 0:
                self.new_population = self.model.getNewPopulation()
            else:
                print("getpop")
                self.new_population = self.model.getPopulation()
            self.model.setAnimal(self.new_population)
            self.fallenAnimals = []
            print(self.fallenAnimals)
            print(len(self.new_population))

        for indexAnimal in range(len(self.new_population)):
            if indexAnimal not in self.fallenAnimals:
                animal = self.new_population[indexAnimal]
                self.top, self.head = animal.getTopBodyAndHeadBody()
                isMoving = animal.isMoving()
                isNotFalling = animal.isNotFalling()
                print(animal,indexAnimal)
                if isMoving and isNotFalling:
                    self.start_time = time()
                    self.model.moves(self.direction, animal)
                    self.distance = self.top.position[0] - animal.getPosition()[0]
                    animal.updateTime()

                else:
                    self.distance_final = self.top.position[0] - animal.getPosition()[0]
                    animal.setScore(self.distance_final) #TODO revoir le score
                    #print("remove " +str(isMoving) +str(isNotFalling)+str(indexAnimal))
                    self.model.removeAnimal(animal)
                    self.fallenAnimals.append(indexAnimal)
                    if self.individu == 1:
                        self.model.sortPopulation()
                        self.model.completeScoreGeneration(self.generation)
                        self.generation += 1
                    self.individu -= 1