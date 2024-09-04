
# Imports
import pygame
import random

# Initialize Pygame
pygame.init()

# Set up screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
CLOCK = pygame.time.Clock()

font1 = pygame.font.Font(None, 36)
font2 = pygame.font.Font(None, 18)

# FPS
FPS = 15

# Set up tile dimensions and number of tiles
TILE_LENGTH = 20  # Width and height divided by length must be an integer
NUM_TILE_X = int(SCREEN_WIDTH / TILE_LENGTH)
NUM_TILE_Y = int(SCREEN_HEIGHT / TILE_LENGTH)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create Screen
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("SNAKE")

# Initialize speed and direction
snake_direction = 'right'
snake_speed = 1


# String  used for empty, apple, and snake
# 'E'
# 'A'
# 'S'

# Create Game Class
class Game:
    running = True
    stopping = False
    score = 0

    @staticmethod
    def run(run_bool):
        Game.running = run_bool

    @staticmethod
    def stop(stop_bool):
        Game.stopping = stop_bool

    @staticmethod
    def add_score():
        Game.score += 1


# Create Board class
class Board:
    # Creates board with all empty tiles
    def __init__(self):
        self.board = [['E' for _ in range(NUM_TILE_Y)] for _ in range(NUM_TILE_X)]

    # Updates position on board for apple
    # x and y are the coordinates of the apple
    @staticmethod
    def update_apple(board_list, x, y):
        board_list[x][y] = 'A'

    # Updates positions on board for snake
    # last_x and last_y are the coordinates of the last block of the snake
    # snake_x and snake_y are lists containing the x and y coordinates for every block of the snake
    @staticmethod
    def update_snake(board_list, snake_x, snake_y, last_x=None, last_y=None):
        for x, y in (zip(snake_x, snake_y)):
            if SCREEN_WIDTH/TILE_LENGTH > x >= 0 and SCREEN_HEIGHT / TILE_LENGTH > y >= 0:
                board_list[x][y] = 'S'
            else:
                Game.stop(True)
        if last_x is not None:
            if last_y is not None:
                board_list[last_x][last_y] = 'E'


class Apple:
    # Initialize apple coordinates and snake object
    def __init__(self, snake_obj):
        self.apple_x = 0
        self.apple_y = 0
        self.snake = snake_obj

    def generate_apple(self, snake_x, snake_y):
        # Random coordinates for new apple
        self.apple_x, self.apple_y = random.randint(0, NUM_TILE_X - 1), random.randint(0, NUM_TILE_Y - 1)
        # Make sure apple location is not on snake and update
        if not self.check_overlap(snake_x, snake_y):
            Board.update_apple(board.board, self.apple_x, self.apple_y)
            self.snake.update_body(self)
            return None

        # Repeat function if apple overlaps
        self.generate_apple(snake_x, snake_y)

    # Checks overlap with snake, returns boolean
    def check_overlap(self, snake_x, snake_y):
        for x, y in zip(snake_x, snake_y):
            if self.apple_x == x and self.apple_y == y:
                return self.apple_x == x and self.apple_y == y


class Snake:
    # Initialize direction, speed, length, board length, location coordinates, and starting location
    def __init__(self, direction, speed, length, num_tile):
        self.direction = [direction]
        self.speed = speed
        self.length = length
        self.num_tile = num_tile

        self.snake_x, self.snake_y = [], []
        (self.snake_x.append(random.randint(0, self.num_tile - 1)),
         self.snake_y.append(random.randint(0, self.num_tile - 1)))
        Board.update_snake(board.board, self.snake_x, self.snake_y)
        Draw.draw_snake(SCREEN, self)

    # Updates coordinates in snake_x and snake_y, returns last coordinate
    def update_body(self, apple_obj):
        if apple_obj.check_overlap(self.snake_x, self.snake_y):
            Game.add_score()
            apple_obj.generate_apple(self.snake_x, self.snake_y)
            last_x, last_y = self.snake_x[-1], self.snake_y[-1]
            if self.direction[-1] == 'right':
                self.snake_x.append(last_x + 1)
                self.snake_y.append(last_y)
            elif self.direction[-1] == 'left':
                self.snake_x.append(last_x - 1)
                self.snake_y.append(last_y)
            elif self.direction[-1] == 'up':
                self.snake_x.append(last_x)
                self.snake_y.append(last_y - 1)
            elif self.direction[-1] == 'down':
                self.snake_x.append(last_x)
                self.snake_y.append(last_y + 1)
            self.direction.append(self.direction[-1])
        last_x, last_y = self.snake_x[-1], self.snake_y[-1]
        for position in range(len(self.snake_x) - 1):
            self.snake_x[len(self.snake_x) - position - 1] = self.snake_x[len(self.snake_x) - position - 2]
        for position in range(len(self.snake_y) - 1):
            self.snake_y[len(self.snake_y) - position - 1] = self.snake_y[len(self.snake_y) - position - 2]
        for position in range(len(self.direction) - 1):
            self.direction[len(self.direction) - position - 1] = self.direction[len(self.snake_x) - position - 2]
        return last_x, last_y

    # Moves snake by calling update_body() based on direction as well as calling update_snake()
    # in the board class
    def move(self, apple_obj):
        if self.direction[0] == 'right':
            last_x, last_y = self.update_body(apple_obj)
            self.snake_x[0] += self.speed
            if len(self.snake_x) != 1:
                Board.update_snake(board.board, self.snake_x, self.snake_y, last_x, last_y)
            else:
                Board.update_snake(board.board, self.snake_x, self.snake_y)
        if self.direction[0] == 'left':
            last_x, last_y = self.update_body(apple_obj)
            self.snake_x[0] -= self.speed
            if len(self.snake_x) != 1:
                Board.update_snake(board.board, self.snake_x, self.snake_y, last_x, last_y)
            else:
                Board.update_snake(board.board, self.snake_x, self.snake_y)
        if self.direction[0] == 'up':
            last_x, last_y = self.update_body(apple_obj)
            self.snake_y[0] -= self.speed
            if len(self.snake_x) != 1:
                Board.update_snake(board.board, self.snake_x, self.snake_y, last_x, last_y)
            else:
                Board.update_snake(board.board, self.snake_x, self.snake_y)
        if self.direction[0] == 'down':
            last_x, last_y = self.update_body(apple_obj)
            self.snake_y[0] += self.speed
            if len(self.snake_x) != 1:
                Board.update_snake(board.board, self.snake_x, self.snake_y, last_x, last_y)
            else:
                Board.update_snake(board.board, self.snake_x, self.snake_y)

    def change_direction(self, direction):
        self.direction[0] = direction


# Draws empty space, snake, and apple
class Draw:
    @staticmethod
    def draw_empty(screen):
        screen.fill(WHITE)

    @staticmethod
    def draw_snake(screen, snake_obj):
        for x, y in zip(snake_obj.snake_x, snake_obj.snake_y):
            pygame.draw.rect(screen, BLUE, (x * NUM_TILE_X, y * NUM_TILE_Y, TILE_LENGTH, TILE_LENGTH))

    @staticmethod
    def draw_apple(screen, apple_obj):
        pygame.draw.rect(screen, RED,
                         (apple_obj.apple_x * NUM_TILE_X,
                          apple_obj.apple_y * NUM_TILE_Y, TILE_LENGTH, TILE_LENGTH))


# Create Board, Snake, and Apple
board = Board()
snake = Snake(snake_direction, snake_speed, TILE_LENGTH, NUM_TILE_X)
apple = Apple(snake)
apple.generate_apple(snake.snake_x, snake.snake_y)


Game.run(True)
Game.stop(False)
first = True

while Game.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Game.running = False
            elif event.key == pygame.K_a:
                if snake.direction[0] != 'right':
                    snake.change_direction('left')
            elif event.key == pygame.K_d:
                if snake.direction[0] != 'left':
                    snake.change_direction('right')
            elif event.key == pygame.K_w:
                if snake.direction[0] != 'down':
                    snake.change_direction('up')
            elif event.key == pygame.K_s:
                if snake.direction[0] != 'up':
                    snake.change_direction('down')

    snake.move(apple)

    Draw.draw_empty(SCREEN)
    Draw.draw_snake(SCREEN, snake)
    Draw.draw_apple(SCREEN, apple)

    text = font2.render(f"Score: {Game.score}", True, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (50, 50)
    SCREEN.blit(text, text_rect)
    pygame.display.flip()

    if first:
        pygame.time.delay(1000)
        first = False

    if Game.stopping:
        while Game.stopping:
            for event in pygame.event.get():
                # Render text (outside the loop)
                text = font1.render("you suck lol press escape!", True, BLACK)
                # Get the text's rectangle
                text_rect = text.get_rect()
                # Center the text on the screen
                text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                # Draw the text on the screen
                SCREEN.blit(text, text_rect)
                # Update the display
                pygame.display.flip()
                if event.type == pygame.QUIT:
                    Game.running = False
                    Game.stopping = False  # Exit the loop
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Game.running = False
                        Game.stopping = False  # Exit the loop

    CLOCK.tick(FPS)
    print(snake.snake_x)
    print(snake.snake_y)

# Quit Pygame
pygame.quit()
