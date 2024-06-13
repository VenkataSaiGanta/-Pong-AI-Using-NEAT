import pygame

class Bars:

    VELOCITY_OF_BAR = 5
    HEIGHT = 100
    WIDTH = 20

    def __init__(self, x, y):
        self.y = self.initial_y = y
        self.x = self.initial_x = x

    def drawBars(self, win):
        pygame.draw.rect(
            win, (0, 0, 139), (self.x, self.y, self.WIDTH, self.HEIGHT))

    def motion(self, up=True):
        if up == False:
            self.y = self.y + self.VELOCITY_OF_BAR

        else:
            self.y = self.y - self.VELOCITY_OF_BAR

    def go_to_initial_state(self):
        self.y = self.initial_y
        self.x = self.initial_x
