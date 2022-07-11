import pygame
import random

pygame.font.init()

# Global Variables
window_width = 800
window_height = 700
play_width = 300
play_height = 600
block_size = 30

top_left_x = (window_width - play_width) // 2
top_left_y = window_height - play_height

"""
Shapes:
Every shape has different rotation models which will be represented by an individual list. 

"""

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# will map the colors to the shapes

class Component(object):
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # possibilities to rotate object(max 3)


def create_grid(occupied_blocks={}):
    # fill 10 x 20 grid, all already occupied blocks will be tracked by dict
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in occupied_blocks:
                tmp = occupied_blocks[(j, i)]
                grid[i][j] = tmp
    return grid


def draw_grid(surface, grid):
    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (top_left_x, top_left_y + i * block_size),
                         (top_left_x + play_width, top_left_y + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (top_left_x + j * block_size, top_left_y),
                             (top_left_x + j * block_size, top_left_y + play_height))


def draw_window(surface, grid, score=0, last_score=0):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont("italic", 60)
    label = font.render("Tetris", True, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width()) / 2, 30))

    # current score
    font = pygame.font.SysFont("italic", 30)
    label = font.render("Score: " + str(score), 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 370

    surface.blit(label, (sx + 20, sy + 150))

    #Highscore
    label = font.render("Highscore: " + str(last_score), 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 400

    surface.blit(label, (sx + 20, sy + 150))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    draw_grid(surface, grid)
    # pygame.display.update()

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont("italic", 30)
    label = font.render("Next Shape", 1, (255,255,255))

    sx = top_left_x + play_width + 70
    sy = top_left_y + play_height / 2
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                pygame.draw.rect(surface, shape.color, (sx + j * block_size, sy + i * block_size, block_size, block_size), 0)
    surface.blit(label, (sx + 10, sy - 30))

def clear_rows(grid, occupied):

    inc = 0
    for i in range(len(grid)-1 ,-1,-1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del occupied[(j,i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(occupied), key = lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                occupied[newKey] = occupied.pop(key)

    return inc

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("italic", size, bold=True)
    label = font.render(text, True, color)

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))

def update_score(new_score):
    score = max_score()

    with open("Score.text", "w") as f:
        if int(score) > new_score:
            f.write(str(score))
        else:
            f.write(str(new_score))

def max_score():
    with open("Score.text", "r") as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    return Component(5, 0, random.choice(shapes))


def format_shapes(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, col in enumerate(row):
            if col == "0":
                positions.append((shape.x + j, shape.y + i))
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    valid_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    valid_pos = [j for sub in valid_pos for j in sub]

    formatted = format_shapes(shape)
    for pos in formatted:
        if pos not in valid_pos:
            if pos[1] > -1:
                return False
    return True


def main(win):
    last_score = max_score()
    occupied_blocks = {}
    grid = create_grid(occupied_blocks)

    change_component = False
    run = True
    current_component = get_shape()
    next_component = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
        grid = create_grid(occupied_blocks)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_component.y += 1
            if not (valid_space(current_component, grid)) and current_component.y > 0:
                current_component.y -= 1
                change_component = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_component.x -= 1
                    if not (valid_space(current_component, grid)):
                        current_component.x += 1
                if event.key == pygame.K_RIGHT:
                    current_component.x += 1
                    if not (valid_space(current_component, grid)):
                        current_component.x -= 1
                if event.key == pygame.K_DOWN:
                    current_component.y += 1
                    if not (valid_space(current_component, grid)):
                        current_component.y -= 1
                if event.key == pygame.K_UP:
                    current_component.rotation += 1
                    if not (valid_space(current_component, grid)):
                        current_component.rotation -= 1
        shape_pos = format_shapes(current_component)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_component.color

        if change_component:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                occupied_blocks[p] = current_component.color
            current_component = next_component
            next_component = get_shape()
            change_component = False
            score += clear_rows(grid, occupied_blocks) * 10

        draw_window(win, grid, score, last_score)
        draw_next_shape(next_component, win)
        pygame.display.update()

        if check_lost(occupied_blocks):
            draw_text_middle(win, "You lost!", 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)


def main_menu(win):
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle(win, "Press Any Key To Pay", 60, (255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)



win = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Tetris")
main_menu(win)
