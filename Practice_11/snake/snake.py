import pygame
import random

pygame.init()

# --- SETTINGS ---
WIDTH, HEIGHT = 600, 600
CELL = 20
SUPER_CELL = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

# --- COLORS ---
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)
PURPLE = (200, 0, 200)

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

def generate_super_food():
    """Generate food NOT on snake"""
    while True:
        x = random.randrange(0, WIDTH, SUPER_CELL)
        y = random.randrange(0, HEIGHT, SUPER_CELL)
        if (x, y) not in snake and (x + 20, y) not in snake and (x, y + 20) not in snake and (x + 20, y + 20) not in snake:
            if (x, y) != food and (x + 20, y) != food and (x, y + 20) != food and (x + 20, y + 20) != food:
                return (x, y)
        
# --- GAME OVER SCREEN ---
def show_game_over():
    screen.fill(WHITE)

    text = game_over_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Score: {score}", True, BLACK)

    screen.blit(text, (WIDTH//2 - 150, HEIGHT//2 - 50))
    screen.blit(score_text, (WIDTH//2 - 60, HEIGHT//2 + 20))

    pygame.display.flip()
    pygame.time.delay(3000)

#adding 2 events to set a timer for super_food
SPAWN_SUPER = pygame.USEREVENT + 1
REMOVE_SUPER = pygame.USEREVENT + 2

pygame.time.set_timer(SPAWN_SUPER, 10000)  # каждые 10 сек

super_food = None
super_active = False

# --- GAME LOOP ---
run = True
while run:
    clock.tick(speed)
    screen.fill(WHITE)

    # --- EVENTS ---
    for event in pygame.event.get():
        
        #removing after 5 seconds
        if event.type == SPAWN_SUPER:
            super_food = generate_super_food()
            super_active = True
            pygame.time.set_timer(REMOVE_SUPER, 5000)  # исчезнет через 5 сек

        #declaring false to remove super_food
        if event.type == REMOVE_SUPER:
            super_food = None
            super_active = False
            
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

    #if super_food is active then we are checking for the collision with the snake
    if super_active:
        x_s, y_s = super_food
        if new_head == super_food or new_head == (x_s, y_s + 20) or new_head == (x_s + 20, y_s) or new_head == (x_s + 20, y_s + 20):
            score += 5
            super_food = None
            super_active = False
    
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
    if super_active: #drawing super food 
        pygame.draw.rect(screen, PURPLE, (*super_food, SUPER_CELL, SUPER_CELL))
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