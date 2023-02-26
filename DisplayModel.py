import pymunk
import pygame
import sys
import pymunk.pygame_util
import Environment
import time

width, height = 1800, 700


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
        while self.running:
            self.setDirection()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == contractMusclesRight:
                    self.display_simulation()
                    self.i += 2
            """ translation = pymunk.Transform()
            translation = translation.translated(
                5,
                0,
            )

            draw_options.transform = (pymunk.Transform.translation(width*0.5, height*0.5)
                                    @ translation
                                    @ pymunk.Transform.translation(-width*0.5, -height*0.5)
                                    ) """

            self.screen.fill(pygame.Color("white"))
            self.space.debug_draw(draw_options)
            # Info and flip screen
            self.screen.blit(self.font.render("fps: " + str(self.clock.get_fps()), True, pygame.Color("black")), (0, 0))
            pygame.display.flip()
            self.space.step(self.dt)
            self.clock.tick(self.fps)
           
    def display_simulation(self):

        if self.new_population == []:
            self.i = 0
            self.direction = 1   
            self.new_population = self.model.getNewPopulation()  
            self.model.addToPopulation(self.new_population)
            self.animal = self.new_population[0]
            self.generation += 1 
            self.start_time = time.time()  
            self.model.setAnimal(self.animal, self.start_time)
        
        self.top, self.head = self.animal.getTopBodyAndHeadBody()
        isMoving = self.model.isMoving()
        isNotFalling = self.model.isNotFalling(self.head)

        if isMoving and isNotFalling:
            self.start_time = time.time()
            if self.i <= 2:
                self.model.moves(self.direction, self.animal)
            elif self.i >= 4:
                self.model.moves(self.direction, self.animal)

        else:
            distance = self.top.position[0] - self.model.getPosition()[0]
            self.animal.setScore(distance) #TODO revoir le score
            self.new_population.remove(self.animal)

            if len(self.new_population) != 0:
                self.animal = self.new_population[0]
                self.start_time = time.time()
                self.model.setAnimal(self.animal, self.start_time) 
            else:
                print(self.generation)
    

