import pymunk
import pygame
import sys
import pymunk.pygame_util
import Environment

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
        

    def show(self):
        i = 0
        j = 0
        draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        contractMusclesRight = pygame.USEREVENT + 1
        timeToMove = 1000
        pygame.time.set_timer(contractMusclesRight, timeToMove, 10)
        while self.running:
            if i == 2:
                i = 0
            if j == 2:
                j = 0
            elif j == 0:
                j = 2 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == contractMusclesRight:
                    print("time to move")
                    self.model.moves(i, j)
            
            self.screen.fill(pygame.Color("white"))
            self.space.debug_draw(draw_options)
            # Info and flip screen
            self.screen.blit(self.font.render("fps: " + str(self.clock.get_fps()), True, pygame.Color("black")), (0, 0))
            pygame.display.flip()
            pygame.display.set_caption("Simulation de marche")
            self.space.step(self.dt)
            self.clock.tick(self.fps)
           
            i += 1
        
