import pygame

class Slider:
    def __init__(self, position: tuple, underValue: int = 0, upperValue: int = 10, sliderWidth: int = 30,
                 text: str = "",
                 outlineSize: tuple = (250, 32)) -> None:
        self.position = position
        self.outlineSize = outlineSize
        self.text = text
        self.sliderWidth = sliderWidth
        self.upperValue = upperValue
        self.underValue = underValue

    # returns the current value of the slider
    def getValue(self) -> float:
        if self.upperValue == self.underValue :
            return self.underValue
        return self.underValue + self.sliderWidth / (self.outlineSize[0] /(self.upperValue - self.underValue))

    # renders slider and the text showing the value of the slider
    def render(self, display: pygame.display, color) -> None:
        # draw outline and slider rectangles
        pygame.draw.rect(display, (200, 220, 255), (self.position[0], self.position[1],
                                                    self.sliderWidth, self.outlineSize[1]))
        pygame.draw.rect(display, color, (self.position[0], self.position[1],
                                              self.outlineSize[0], self.outlineSize[1]), 3)

        # determite size of font
        self.font = pygame.font.SysFont("Arial", int(self.outlineSize[1]/2))

        # create text surface with value
        valueSurf = self.font.render(f"{self.text}: {round(self.getValue())}", True, color)

        # centre text
        textx = self.position[0] + (self.outlineSize[0] / 2) - (valueSurf.get_rect().width / 2)
        texty = self.position[1] + (self.outlineSize[1] / 2) - (valueSurf.get_rect().height / 2)

        display.blit(valueSurf, (textx, texty))

    # allows users to change value of the slider by dragging it.
    def changeValue(self) -> None:
        # If mouse is pressed and mouse is inside the slider
        mousePos = pygame.mouse.get_pos()
        if self.pointInRectanlge(mousePos[0], mousePos[1]
                , self.outlineSize[0], self.outlineSize[1], self.position[0], self.position[1]):
            if pygame.mouse.get_pressed()[0]:
                # the size of the slider
                self.sliderWidth = mousePos[0] - self.position[0]

                # limit the size of the slider
                if self.sliderWidth < 1:
                    self.sliderWidth = random_factor_current
                if self.sliderWidth > self.outlineSize[0]:
                    self.sliderWidth = self.outlineSize[0]

    def pointInRectanlge(self, px, py, rw, rh, rx, ry):
        if px > rx and px < rx + rw:
            if py > ry and py < ry + rh:
                return True
        return False
