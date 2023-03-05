import pygame
from Model import *
from DisplayModel import *


class Menu:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("Arial", 26)
        self.fps = 60
        self.dt = 1.0 / self.fps

    def intro(self):
        start_button_active_img = pygame.image.load("./imgs/button_active.png").convert_alpha()
        start_button_inactive_img = pygame.image.load("./imgs/button_inactive.png").convert_alpha()
        title_img = pygame.image.load("./imgs/welcome.png").convert_alpha()
        x_pos = 500
        y_pos = 150
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            self.screen.fill(pygame.Color("white"))
            titleText = self.screen.blit(title_img, (x_pos-80, y_pos-20))  # Title is an image
            titleText.center = ((x_pos+350), (y_pos+130))
            self.button(x_pos+200, y_pos+330, 195, 80, start_button_inactive_img, start_button_active_img, self.menu)
            self.screen.blit(self.font.render("Developers : Azmar Samir & Fernandes do Rosario Tiago & Grégoire Jean-Nicolas & Deneuville Walter"
                                              , True, pygame.Color("black")), (0, 0))
            pygame.display.flip()
            pygame.display.set_caption("Simulation de marche")
            pygame.display.update()
            self.clock.tick(self.fps)
        pygame.quit()

    def menu(self): 
        start_button_active_img = pygame.image.load("./imgs/button_active.png").convert_alpha()
        start_button_inactive_img = pygame.image.load("./imgs/button_inactive.png").convert_alpha()
        x_pos = 300
        y_pos = 100
        y_offset = 70
        number_boxes = 5
        label_boxes = ["Mutation probability :", "Foot number :", "Weight :", "Width body :", "Height Body :"]
        default_val_boxes = ["0.1", "4", "100", "200", "100"]
        input_box = [[label_boxes[i], pygame.Rect(x_pos, y_pos+y_offset*i, 140, 32)] for i in range(number_boxes)]
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = [color_inactive for i in range(number_boxes)]
        active = [False for i in range(number_boxes)]
        text = [default_val_boxes[i] for i in range(number_boxes)]
        done = False

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(input_box)):
                        if input_box[i][1].collidepoint(event.pos) and i != 1:
                            active[i] = True
                        else:
                            active[i] = False
                        color[i] = color_active if active[i] else color_inactive
                if event.type == pygame.KEYDOWN:
                    for i in range(len(input_box)):
                        if active[i] and i != 1:
                            if event.key == pygame.K_BACKSPACE:
                                text[i] = text[i][:-1]
                            else:
                                text[i] += event.unicode
            self.screen.fill((255, 255, 255))
            done = self.button(x_pos, y_pos + y_offset*(number_boxes+1), 195, 80, start_button_inactive_img, start_button_active_img, self.clicked)

            if done:
                self.model = Model(float(text[0]), int(text[1]), int(text[2]), int(text[3]), int(text[4]))
                displaymodel = Display(self.model)
                displaymodel.show()
                
            for i in range(number_boxes):
                txt_surface = self.font.render(text[i], True, color[i])
                txt_surface2 = self.font.render(input_box[i][0], True, color[i])
                width = max(200, txt_surface.get_width() + 10)
                input_box[i][1].w = width
                self.screen.blit(txt_surface, (input_box[i][1].x + 5, input_box[i][1].y + 5))
                self.screen.blit(txt_surface2, (input_box[i][1].x - 250, input_box[i][1].y + 5))
                pygame.draw.rect(self.screen, color[i], input_box[i][1], 2)
            pygame.display.flip()
            self.clock.tick(self.fps)

    def button(self, x, y, w, h, inactive, active, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            self.screen.blit(active, (x+40, y))
            if click[0] == 1 and action is not None:
                return action()
        else:
            self.screen.blit(inactive, (x, y))

    def clicked(self):
        return True
