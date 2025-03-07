from random import choice

import pygame

# ПРОВЕРЯЮЩЕМУ. В коммитах вы можете увидеть вариант без фичей

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Список всех ячеек
SEQUENCE = [
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH)
    for y in range(GRID_HEIGHT)
]

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки"""
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки
SPEED = 5

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля
pygame.display.set_caption('Змейка')

# Настройка времени
clock = pygame.time.Clock()


class GameObject:
    """Основной (родительский) класс игрового объекта."""

    def __init__(self):
        """Инициализация."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = (0, 0, 0)

    def draw(self):
        """Метод отрисовки."""
        pass


class Apple(GameObject):
    """Дочерний класс Яблока."""

    def __init__(self):
        """Инициализация."""
        super().__init__()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Метод, задающий Яблоку случайную позицию."""
        self.position = choice(SEQUENCE)

    def draw(self):
        """Метод отрисовки яблока."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Trash(GameObject):
    """Дочерний класс Мусора."""

    def __init__(self):
        """Инициализация."""
        super().__init__()
        self.body_color = (198, 195, 181)
        self.position = (620, 460)

    def randomise_position(self):
        """Метод, задающий Мусору случайную позицию."""
        self.position = choice(SEQUENCE)

    def draw(self):
        """Метод отрисовки Мусора."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Дочерний класс Змейки."""

    def __init__(self):
        """Инициализация."""
        super().__init__()
        self.position = (0, 0)
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.positions = list()
        self.positions.append((self.position))
        self.last = None

    def update_direction(self):
        """Метод обновления движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод движения."""
        head = self.get_head_position()

        if head[0] == 0 and self.direction == LEFT:
            cell = (SCREEN_WIDTH - GRID_SIZE, head[1])
        elif head[0] == (SCREEN_WIDTH - GRID_SIZE) and self.direction == RIGHT:
            cell = (0, head[1])
        elif head[1] == 0 and self.direction == UP:
            cell = (head[0], SCREEN_HEIGHT - GRID_SIZE)
        elif head[1] == (SCREEN_HEIGHT - GRID_SIZE) and self.direction == DOWN:
            cell = (head[0], 0)
        else:
            cell = (
                head[0] + self.direction[0] * 20,
                head[1] + self.direction[1] * 20,
            )

        self.positions.insert(0, cell)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Метод отрисовки змейки."""
        for position in self.positions:
            rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод, возвращающий координаты головы."""
        return self.positions[0]

    def reset(self):
        """Метод, сбрасывающий все атрибуты."""
        self.position = (0, 0)
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.positions = list()
        self.positions.append((self.position))
        self.last = None


def handle_keys(game_object):
    """Функция на обработку входных данных(клавиш)."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная логика игры."""
    speed = int(input('Введите желаемую скорость игры:'))

    pygame.init()

    snake = Snake()
    apple = Apple()
    trash = Trash()

    while True:

        clock.tick(speed)

        handle_keys(snake)
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:

            snake.length += 1
            apple.randomize_position()

            while apple.position in snake.positions:
                apple.randomize_position()

        if snake.get_head_position() == trash.position:

            snake.length -= 1
            trash.randomise_position()
            snake.positions = snake.positions[:-1]

            while (trash.position in snake.positions) or (
                apple.position == trash.position
            ):
                trash.randomize_position()

        if snake.length < 1:
            snake.reset()
            apple.randomize_position()

        snake.draw()
        apple.draw()
        trash.draw()
        pygame.display.update()

        if len(snake.positions) != len(set(snake.positions)):
            snake.reset()
            apple.randomize_position()


if __name__ == '__main__':
    """Запуск игры."""
    main()
