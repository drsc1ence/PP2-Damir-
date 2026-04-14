import pygame
import random

pygame.init()

# --- SETTINGS ---
WIDTH, HEIGHT = 600, 600
CELL = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

# --- COLORS ---
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

# --- FONTS ---
font = pygame.font.SysFont("Verdana", 20)
game_over_font = pygame.font.SysFont("Verdana", 50)

# --- INITIAL STATE ---
snake = [(100, 100)]
direction = (CELL, 0)

score = 0
level = 1
speed = 5

# --- GENERATE FOOD ---
def generate_food():
    """Generate food NOT on snake"""
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)
        if (x, y) not in snake:
            return (x, y)

food = generate_food()

# --- GAME OVER SCREEN ---
def show_game_over():
    screen.fill(WHITE)

    text = game_over_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Score: {score}", True, BLACK)

    screen.blit(text, (WIDTH//2 - 150, HEIGHT//2 - 50))
    screen.blit(score_text, (WIDTH//2 - 60, HEIGHT//2 + 20))

    pygame.display.flip()
    pygame.time.delay(3000)


# --- GAME LOOP ---
run = True
while run:
    clock.tick(speed)
    screen.fill(WHITE)

    # --- EVENTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL):
                direction = (0, -CELL)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL):
                direction = (0, CELL)
            elif event.key == pygame.K_LEFT and direction != (CELL, 0):
                direction = (-CELL, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL, 0):
                direction = (CELL, 0)

    # --- MOVE SNAKE ---
    head_x = snake[0][0] + direction[0]
    head_y = snake[0][1] + direction[1]
    new_head = (head_x, head_y)

    # --- WALL COLLISION ---
    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        show_game_over()
        run = False

    # --- SELF COLLISION ---
    if new_head in snake:
        show_game_over()
        run = False

    snake.insert(0, new_head)

    # --- FOOD COLLISION ---
    if new_head == food:
        score += 1
        food = generate_food()

        # --- LEVEL SYSTEM ---
        if score % 4 == 0:
            level += 1
            speed += 2

    else:
        snake.pop()

    # --- DRAW FOOD ---
    pygame.draw.rect(screen, RED, (*food, CELL, CELL))

    # --- DRAW SNAKE ---
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL, CELL))

    # --- DRAW UI ---
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 30))

    pygame.display.flip()

pygame.quit()