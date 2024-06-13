import pygame
import random
from .ball import GameBall
from .bar import Bars
pygame.init()


class gameStatus:
    def __init__(self, left_point, right_point, left_touch, right_touch):
        self.left_touch = left_touch
        self.right_touch = right_touch
        self.left_point = left_point
        self.right_point = right_point


class Play:

    FONT = pygame.font.SysFont("arial", 50)
    BLUE = (0, 0, 139)
    WHITE = (255, 255, 255)

    def __init__(self, arena, arena_width, arena_height):
        self.arena_width = arena_width
        self.arena_height = arena_height

        self.left_bar = Bars(
            10, self.arena_height // 2 - Bars.HEIGHT // 2)
        self.right_bar = Bars(
            self.arena_width - 10 - Bars.WIDTH, self.arena_height // 2 - Bars.HEIGHT//2)
        self.ball = GameBall(self.arena_width // 2, self.arena_height // 2)

        self.left_point = 0
        self.right_point = 0
        self.left_touch = 0
        self.right_touch = 0
        self.arena = arena

    def print_point(self):
        right_point_text = self.FONT.render(
            f"{self.right_point}", 1, self.BLUE)
        left_point_text = self.FONT.render(
            f"{self.left_point}", 1, self.BLUE)
        self.arena.blit(left_point_text, (self.arena_width //
                                          4 - left_point_text.get_width()//2, 20))
        self.arena.blit(right_point_text, (self.arena_width * (3/4) -
                                           right_point_text.get_width()//2, 20))

    def manage_hits(self):
        ball = self.ball
        left_bar = self.left_bar
        right_bar = self.right_bar

        if ball.y - ball.RADIUS_OF_BALL <= 0:
            ball.curr_y_velocity *= -1
        elif ball.y + ball.RADIUS_OF_BALL >= self.arena_height:
            ball.curr_y_velocity *= -1

        if ball.curr_x_velocity >= 0:
            if ball.y >= right_bar.y and ball.y <= right_bar.y + Bars.HEIGHT:
                if ball.x + ball.RADIUS_OF_BALL >= right_bar.x:
                    ball.curr_x_velocity *= -1

                    middle_y = right_bar.y + Bars.HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (Bars.HEIGHT / 2) / ball.VELOCITY
                    y_VELOCITY_OF_BAR = difference_in_y / reduction_factor
                    ball.y_VELOCITY_OF_BAR = -1 * y_VELOCITY_OF_BAR
                    self.right_touch += 1

        else:
            if ball.y >= left_bar.y and ball.y <= left_bar.y + Bars.HEIGHT:
                if ball.x - ball.RADIUS_OF_BALL <= left_bar.x + Bars.WIDTH:
                    ball.curr_x_velocity *= -1

                    middle_y = left_bar.y + Bars.HEIGHT / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (Bars.HEIGHT / 2) / ball.VELOCITY
                    y_VELOCITY_OF_BAR = difference_in_y / reduction_factor
                    ball.y_VELOCITY_OF_BAR = -1 * y_VELOCITY_OF_BAR
                    self.left_touch += 1

    def draw(self, draw_score=True):
        self.arena.fill(self.WHITE)

        if draw_score:
            self.print_point()

        for Bars in [self.left_bar, self.right_bar]:
            Bars.drawBars(self.arena)

        self.ball.drawBall(self.arena)

    def move_Bars(self, left=True, up=True):

        if left == False:
            if up and self.right_bar.y - Bars.VELOCITY_OF_BAR < 0:
                return False
            if not up and self.right_bar.y + Bars.HEIGHT > self.arena_height:
                return False
            self.right_bar.motion(up)

        else:
            if up and self.left_bar.y - Bars.VELOCITY_OF_BAR < 0:
                return False
            if not up and self.left_bar.y + Bars.HEIGHT > self.arena_height:
                return False
            self.left_bar.motion(up)

        return True

    def loop(self):

        self.ball.motion()
        self.manage_hits()
        if self.ball.x > self.arena_width:
            self.ball.go_to_initial_state()
            self.left_point += 1
        elif self.ball.x < 0:
            self.ball.go_to_initial_state()
            self.right_point += 1

        game_info = gameStatus(self.left_point, self.right_point,
                               self.left_touch, self.right_touch)

        return game_info

    def go_to_initial_state(self):

        self.ball.go_to_initial_state()
        self.left_bar.go_to_initial_state()
        self.right_bar.go_to_initial_state()
        self.left_point = 0
        self.right_point = 0
        self.left_touch = 0
        self.right_touch = 0
