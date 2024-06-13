import pygame
import random
import math

class GameBall:
    VELOCITY = 6
    RADIUS_OF_BALL = 7

    def __init__(self, x, y):
        self.x = self.initial_x = x
        self.y = self.initial_y = y

        position = 1 if random.random() < 0.5 else -1

        angle = self.takeRandomAngle(-30, 30, [0])

        self.curr_x_velocity = abs(math.cos(angle) * self.VELOCITY)*position

        self.curr_y_velocity = self.VELOCITY * math.sin(angle)

    def drawBall(self, win):
        pygame.draw.circle(
            win, (0, 0, 139), (self.x, self.y), self.RADIUS_OF_BALL)

    def motion(self):
        self.y = self.y + self.curr_y_velocity
        self.x = self.x + self.curr_x_velocity

    def takeRandomAngle(self, min_angle, max_angle, excluded):
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))

        return angle

    def go_to_initial_state(self):
        self.y = self.initial_y
        self.x = self.initial_x

        angle = self.takeRandomAngle(-30, 30, [0])
        curr_y_velocity = math.sin(angle) * self.VELOCITY
        curr_x_velocity = abs(math.cos(angle) * self.VELOCITY)

        self.curr_x_velocity = self.curr_x_velocity * -1
        self.curr_y_velocity = curr_y_velocity
