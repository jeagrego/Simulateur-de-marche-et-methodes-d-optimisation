import pygame
from Model import *
from DisplayModel import *
from constantes import *
from Slider import *


class Menu:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("Arial", 26)
        self.fps = 60
        self.dt = 1.0 / self.fps
        self.x_pos = 300 + (width * 0.35)
        self.y_pos = 100
        self.y_offset = 70
        self.number_boxes = 6
        self.default_val_boxes = ["0.1", "4", "100", "200", "100", "1"]
        self.min_max_values = [[0, 100, 20], [4, 4, 0], [100, 200, 0], [100, 300, 100], [100, 200, 0], [1, 2, 1]]
        self.label_boxes = ["Mutation probability(%) :", "Foot number :", "Weight(kg) :", "Width body(pixels) :",
                            "Height Body(pixels) :", "Algorithm :"]
        self.text = [self.default_val_boxes[i] for i in range(self.number_boxes)]
        self.input_box = [[self.label_boxes[i], pygame.Rect(self.x_pos, self.y_pos + self.y_offset * i, 240, 32)] for i
                          in range(self.number_boxes)]
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color = [self.color_inactive for i in range(self.number_boxes)]
        self.start_button_active_img = pygame.image.load("../resources/imgs/envoyer_active.png").convert_alpha()
        self.start_button_inactive_img = pygame.image.load("../resources/imgs/envoyer_inactive.png").convert_alpha()

    def intro(self):
        title_img = pygame.image.load("../resources/imgs/welcome.png").convert_alpha()
        x_pos = 500
        y_pos = 150
        start_time = time()
        end_intro = 0
        while end_intro < 5:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            self.screen.fill(pygame.Color("white"))
            titleText = self.screen.blit(title_img, (x_pos - 80, y_pos - 20))  # Title is an image
            titleText.center = ((x_pos + 350), (y_pos + 130))
            # self.button(x_pos+200, y_pos+330, 195, 80, self.start_button_inactive_img, self.start_button_active_img, self.menu)
            self.screen.blit(self.font.render(
                "Developers : Azmar Samir & Fernandes do Rosario Tiago & Grégoire Jean-Nicolas & Deneuville Walter"
                , True, pygame.Color("black")), (0, 0))
            pygame.display.flip()
            pygame.display.set_caption("Simulation de marche")
            pygame.display.update()
            self.clock.tick(self.fps)
            end_intro = time() - start_time
        self.menu()
        pygame.quit()

    def menu(self):
        color_active = pygame.Color('dodgerblue2')
        active = [False for i in range(self.number_boxes)]
        isDone = False
        sliders = [
            Slider((self.x_pos, self.y_pos + self.y_offset * i), self.min_max_values[i][0], self.min_max_values[i][1],
                   self.min_max_values[i][2], "", (200, 32)) for i in range(self.number_boxes)]
        values = ["" for i in range(self.number_boxes)]
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(self.input_box)):
                        if self.input_box[i][1].collidepoint(event.pos) and i != 1:
                            active[i] = True
                        else:
                            active[i] = False
                        self.color[i] = color_active if active[i] else self.color_inactive
            self.screen.fill((255, 255, 255))
            isDone = self.boolButton()
            for i in range(len(sliders)):
                sliders[i].render(self.screen, self.color[i])
                sliders[i].changeValue()
                values[i] = str(sliders[i].getValue())
            if round(sliders[5].getValue()) == 1:  # Box algorithm
                self.input_box[0][0] = "Mutation probability(%) :"
            if round(sliders[5].getValue()) == 2:  # Box algorithm
                self.input_box[0][0] = "Randomness Factor(%) :"
            if isDone:
                self.drawModel(values)
            self.drawOptions()
            pygame.display.flip()
            self.clock.tick(self.fps)

    def boolButton(self):
        y = self.y_pos + self.y_offset * (self.number_boxes + 1)
        return self.button(self.x_pos - 150, y, 464, 140, self.start_button_inactive_img, self.start_button_active_img,
                           self.clicked)

    def drawModel(self, values):
        self.model = Model(float(values[0]), int(values[1]), float(values[2]), float(values[3]), float(values[4]), round(float(values[5])))
        displaymodel = Display(self.model)
        displaymodel.show()

    def drawOptions(self):
        for i in range(self.number_boxes):
            txt_surface = self.font.render(self.text[i], True, self.color[i])
            txt_surface2 = self.font.render(self.input_box[i][0], True, self.color[i])
            width = max(200, txt_surface.get_width() + 10)
            self.input_box[i][1].w = width
            self.screen.blit(txt_surface2, (self.input_box[i][1].x - 250, self.input_box[i][1].y + 5))
            pygame.draw.rect(self.screen, self.color[i], self.input_box[i][1], 2)

    def button(self, x, y, w, h, inactive, active, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        self.screen.blit(inactive, (x, y))

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            if click[0] == 1 and action is not None:
                return action()

            else:
                self.screen.blit(active, (x, y))

    def clicked(self):
        return True
