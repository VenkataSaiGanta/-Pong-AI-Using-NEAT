# SUBHAM MAJUMDER
# GITHUB- https://github.com/bits-and-atoms

from pong import Play
import pygame
import pickle
import neat
import os

# Refer to https://neat-python.readthedocs.io/en/latest/config_file.html for setting up configuration file
# Thanks to neat documentation - https://neat-python.readthedocs.io/en/latest/neat_overview.html


class PlayPong:

    def __init__(self, window, width, height):
        self.game = Play(window, width, height)
        self.left_bar = self.game.left_bar
        self.right_bar = self.game.right_bar
        self.ball = self.game.ball

    def testing(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.game.move_Bars(left=True, up=True)
            if keys[pygame.K_DOWN]:
                self.game.move_Bars(left=True, up=False)

            output = net.activate(
                (self.right_bar.y, self.ball.y, abs(self.right_bar.x - self.ball.x)))
            decision = output.index(max(output))

            if decision == 0:
                pass
            elif decision == 1:
                self.game.move_Bars(left=False, up=True)
            else:
                self.game.move_Bars(left=False, up=False)

            game_info = self.game.loop()
            self.game.draw(True)
            pygame.display.update()

        # pygame.quit()

    def training(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            output1 = net1.activate(
                (self.left_bar.y, self.ball.y, abs(self.left_bar.x - self.ball.x)))
            decision1 = output1.index(max(output1))

            if decision1 == 1:
                self.game.move_Bars(left=True, up=True)
            elif decision1 == 0:
                pass
            else:
                self.game.move_Bars(left=True, up=False)

            output2 = net2.activate(
                (self.right_bar.y, self.ball.y, abs(self.right_bar.x - self.ball.x)))
            decision2 = output2.index(max(output2))

            if decision2 == 1:
                self.game.move_Bars(left=False, up=True)
            elif decision2 == 0:
                pass
            else:
                self.game.move_Bars(left=False, up=False)

            game_info = self.game.loop()

            self.game.draw(draw_score=False)
            pygame.display.update()

            if game_info.left_point >= 1 or game_info.right_point >= 1 or game_info.left_touch > 50:
                self.calculate_fitness(genome1, genome2, game_info)
                break

    def calculate_fitness(self, genome1, genome2, game_info):
        genome1.fitness += game_info.left_touch
        genome2.fitness += game_info.right_touch


def eval_genomes(genomes, config):
    width, height = 700, 500
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Subham's Pong")
    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game = PlayPong(window, width, height)
            game.training(genome1, genome2, config)


def run_neat(config):
    # uncomment below line if you want to continue training from some particular checkpoint but after that comment the line p = neat.Population(config)
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-21')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 50)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


def testing(config):
    width, height = 700, 500
    window = pygame.display.set_mode((width, height))
    with open("best.pickle", "rb") as f:
        winner = pickle.load(f)
    game = PlayPong(window, width, height)
    game.testing(winner, config)


if __name__ == "__main__":
    config_path = os.path.join("config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    # uncomment below line to train ai
    # run_neat(config)
    # use below line to test the game
    testing(config)
