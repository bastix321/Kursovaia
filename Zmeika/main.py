from ursina import *
from game_objects import *

import pygame
pygame.init()

score_font = pygame.font.SysFont("comicsansms", 35)

class Game(Ursina):
    def __init__(self):
        super().__init__()
        window.color = color.black
        window.fullscreen_size = 1920, 1080
        window.fullscreen = True
        Light(type='ambient', color=(0.5, 0.5, 0.5, 1))
        Light(type='directional', color=(0.5, 0.5, 0.5, 1), direction=(1, 1, 1))
        self.MAP_SIZE = 20
        self.new_game()
        camera.position = (self.MAP_SIZE // 2, -20.5, -20)
        camera.rotation_x = -57


    def create_map(self, MAP_SIZE):
        Entity(model='quad', scale=MAP_SIZE, position=(MAP_SIZE // 2, MAP_SIZE // 2, 0), color=color.dark_gray)
        Entity(model=Grid(MAP_SIZE, MAP_SIZE), scale=MAP_SIZE,
               position=(MAP_SIZE // 2, MAP_SIZE // 2, -0.01), color=color.white)

    def new_game(self):
        scene.clear()
        self.create_map(self.MAP_SIZE)
        self.apple = Apple(self.MAP_SIZE, model='sphere', color=color.red)
        self.snake = Snake(self.MAP_SIZE)
        self.snake2 = Snake2(self.MAP_SIZE)

    def input(self, key):
        if key == 'e':
            camera.rotation_x = 0
            camera.position = (self.MAP_SIZE // 2, self.MAP_SIZE // 2, -50)
        elif key == 'q':
            camera.position = (self.MAP_SIZE // 2, -20.5, -20)
            camera.rotation_x = -57
        super().input(key)

    def check_apple_eaten(self):
        if self.snake.segment_positions[-1] == self.apple.position:
            self.snake.add_segment()
            self.apple.new_position()
        if self.snake2.segment_positions[-1] == self.apple.position:
            self.snake2.add_segment()
            self.apple.new_position()

    def check_game_over(self):
        snake = self.snake.segment_positions
        if 0 < snake[-1][0] < self.MAP_SIZE and 0 < snake[-1][1] < self.MAP_SIZE and len(snake) == len(set(snake)):
                return
                print_on_screen('GAME OVER', position=(-0.7, 0.1), scale=10, duration=1)
        self.snake.direction = Vec3(0, 0, 0)
        self.snake.permissions = dict.fromkeys(self.snake.permissions, 0)
        invoke(self.new_game, delay=1)
        snake2 = self.snake2.segment_positions
        if 0 < snake2[-1][0] < self.MAP_SIZE and 0 < snake2[-1][1] < self.MAP_SIZE and len(snake2) == len(set(snake2)):
            return
            print_on_screen('GAME OVER', position=(-0.7, 0.1), scale=10, duration=1)
        self.snake2.direction = Vec3(0, 0, 0)
        self.snake2.permissions = dict.fromkeys(self.snake2.permissions, 0)
        invoke(self.new_game, delay=1)

    def update(self):
        #print_on_screen(f'Score: {self.snake.score}', position=(-0.85, 0.45), scale=3, duration=1 / 20)
        self.check_apple_eaten()
        self.check_game_over()
        self.snake.run()
        self.snake2.run()


if __name__ == '__main__':
    game = Game()
    update = game.update
    game.run()
    #Your_score(Length_of_snake - 1)
