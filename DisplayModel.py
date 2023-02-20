import pymunk
import pygame
import sys
import pymunk.pygame_util
import Environment
import time

width, height = 1200, 700


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
        self.generation = 1
        self.new_population = []
        self.translation = pymunk.Transform()
        self.i = 0
        self.direction = 1   

    def show(self):
        draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        contractMusclesRight = pygame.USEREVENT + 1
        timeToMove = 500
        pygame.time.set_timer(contractMusclesRight, timeToMove, 100)
        #self.new_population = []
        #self.model.getNewPopulation()
        while self.running:
            if self.i == 2:
                self.direction = 2
            if self.i  == 4:
                self.direction = -1
            if self.i  == 6:
                self.direction = -2
            if self.i >= 8:
                self.i = 0
                self.direction = 1  
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == contractMusclesRight:
                    #print("time to move")
                    self.display_simulation(self.i, self.direction)
                    self.i += 2

            #print(self.generation)
            self.screen.fill(pygame.Color("white"))
            self.space.debug_draw(draw_options)
            # Info and flip screen
            self.screen.blit(self.font.render("fps: " + str(self.clock.get_fps()), True, pygame.Color("black")), (0, 0))
            pygame.display.flip()
            pygame.display.set_caption("Simulation de marche")
            self.space.step(self.dt)
            self.clock.tick(self.fps)
           
    def display_simulation(self, i, direction):

        if self.new_population == []:
            self.i = 0
            self.direction = 1   
            self.new_population = self.model.getNewPopulation()  
            self.model.addToPopulation(self.new_population)
            self.start_time = time.time()
            self.animal = self.new_population[0]
            self.generation += 1   
            self.model.setAnimal(self.animal)
        
        top, head = self.animal.getTopBodyAndHeadBody()
        isMoving = self.model.isMoving(self.start_time , top)
        isFalling = self.model.isFalling(head)

        if isMoving and isFalling:
            if i <= 2:
                self.model.moves(0, self.direction, self.animal)
            elif i >= 4:
                self.model.moves(4, self.direction, self.animal)

        else:
            distance = top.position[0] - self.model.getPosition()[0]
            self.animal.setScore(distance)
            self.new_population.remove(self.animal)

            if len(self.new_population) != 0:
                self.animal = self.new_population[0]
                self.model.setAnimal(self.animal) 
                self.generation += 1
                self.start_time = time.time()
                print(self.generation)
            #print("You are to fat, go to the gym")
        self.translation = self.translation.translated(width-self.animal.getPosition()[0], 0)
        self.space.transform = (
            pymunk.Transform.translation(width*0.5, height*0.5)
            @ self.translation
            @ pymunk.Transform.translation(-width*0.5, -height*0.5)
        )
