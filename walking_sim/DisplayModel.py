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
        self.generation = 0
        self.distance = 0
        self.individu = 0
        self.score = 0
        pygame.display.set_caption("Simulation de marche")
        self.top = pymunk.Body()

    def show(self):
        draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        back_button = pygame.image.load("../resources/imgs/back_arrow.png").convert_alpha()
        back_button_active = pygame.image.load("../resources/imgs/back_arrow_active.png").convert_alpha()
        finish_line = pygame.image.load("../resources/imgs/finish_line.png").convert_alpha()
        grass = pygame.image.load("../resources/imgs/grass1.png").convert_alpha()
        sky = pygame.image.load("../resources/imgs/sky.jpg").convert_alpha()
        x = 50
        y = 50
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            self.screen.fill(pygame.Color("blue"))
            self.screen.blit(finish_line, (1200, 350))
            # back button
            self.screen.blit(back_button, (x, y))
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if x + 80 > mouse[0] > x and y + 70 > mouse[1] > y:
                if click[0] == 1:
                    return
                self.screen.blit(back_button_active, (x, y))
            # end back button
            self.generation, self.individu = self.model.run_simulation()
            self.score = self.model.getBestScore()
            self.space.debug_draw(draw_options)
            self.screen.blit(grass, (0, 560))
            # Info and flip screen
            self.screen.blit(self.font.render(
                "generation :" + str(self.generation) + " individu: " + str(self.individu) + " Best Score: " + str(
                    self.score)
                , True, pygame.Color("black")), (0, 0))
            pygame.display.flip()

            self.space.step(self.dt)
            self.clock.tick(self.fps)
