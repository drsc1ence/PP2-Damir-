#creating db, config and game library by ourselves and using it 
import pygame
import json
import db
from config import *
from game import SnakeGame

#initializing
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Impact", 30)
large_font = pygame.font.SysFont("Impact", 60)

#loading json file for the game
def load_settings():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except:
        return {"snake_color": [0, 200, 0], "grid_overlay": True, "sound": True}

#transferring from python to json
def save_settings(s):
    with open("settings.json", "w") as f:
        json.dump(s, f)

#bringing out texts
def draw_text(txt, pos, color=BLACK, center=False):
    img = font.render(txt, True, color)
    if center:
        pos = img.get_rect(center=pos)
    screen.blit(img, pos)

#displaying menu
def main_menu():
    username = ""
    settings = load_settings()
    
    while True:
        screen.fill(LIGHT_BLUE)
        #displaying menu's text to start a game
        draw_text("ZHYLAN", (WIDTH//2, 100), PINK, True)
        draw_text(f"Enter Username: {username}", (WIDTH//2, 200), BLACK, True)
        draw_text("[SPACE] Play  [1] Leaderboard  [2] Settings", (WIDTH//2, 350), BLACK, True)
        
        #press specific key to start a game, to see ledearboard and to see settings of the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and username: return ("GAME", username)
                if event.key == pygame.K_1: return ("LEADER", None)
                if event.key == pygame.K_2: return ("SETTINGS", None)
                if event.key == pygame.K_BACKSPACE: username = username[:-1]
                elif event.unicode.isalnum() and len(username) < 15:
                    username += event.unicode
        pygame.display.flip()

#function to play a game
def play_game(username):
    settings = load_settings()
    game = SnakeGame(username, settings)
    pb = db.get_personal_best(username)
    
    #loop where i can control snake by pressing keys
    running = True
    while running:
        clock.tick(game.speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return "MENU"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game.direction != (0, CELL): game.direction = (0, -CELL)
                if event.key == pygame.K_DOWN and game.direction != (0, -CELL): game.direction = (0, CELL)
                if event.key == pygame.K_LEFT and game.direction != (CELL, 0): game.direction = (-CELL, 0)
                if event.key == pygame.K_RIGHT and game.direction != (-CELL, 0): game.direction = (CELL, 0)

        #if snake doesnt move then we are ending the game and saving the result
        if not game.move():
            db.save_result(username, game.score, game.level)
            return "GAMEOVER", game.score, game.level, pb

        # Drawing
        screen.fill(LIGHT_BLUE)
        if settings['grid_overlay']:
            for x in range(0, WIDTH, CELL): pygame.draw.line(screen, (240, 240, 240), (x, 0), (x, HEIGHT))
        
        # Entities
        for w in game.walls: pygame.draw.rect(screen, GRAY, (*w, CELL, CELL))
        pygame.draw.rect(screen, RED, (*game.food, CELL, CELL))
        pygame.draw.rect(screen, PINK, (*game.poison, CELL, CELL)) #changed color to pink
        if game.powerup: pygame.draw.rect(screen, BLUE, (*game.powerup, CELL, CELL))
        
        #frawing the snake
        for i, seg in enumerate(game.snake):
            color = tuple(settings['snake_color']) if not game.shield_active or i > 0 else (255, 215, 0)
            pygame.draw.rect(screen, color, (*seg, CELL, CELL))

        draw_text(f"Score: {game.score}  LVL: {game.level}  PB: {pb}", (10, 10))
        pygame.display.flip()

#function that shows us a leaderboard
def show_leaderboard():
    while True:
        screen.fill(LIGHT_BLUE)
        draw_text("TOP 10 PLAYERS", (WIDTH//2, 50), BLACK, True)
        data = db.get_leaderboard()
        #enumerating and placing them one under another
        for i, row in enumerate(data):
            draw_text(f"{i+1}. {row[0]} - {row[1]} pts (Lvl {row[2]})", (WIDTH//2, 100 + i*30), BLACK, True)
        
        #pressing esc key to return to the menu
        draw_text("Press ESC to Back", (WIDTH//2, 550), RED, True)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return
        pygame.display.flip()

def settings_screen(screen):
    font = pygame.font.SysFont("Impact", 40)
    small_font = pygame.font.SysFont("Impact", 30)

    settings = load_settings()

    # Preset colors to cycle through
    colors = [
        (0, 200, 0),
        (200, 0, 0),
        (0, 0, 255),
        (255, 165, 0),
        (200, 0, 200)
    ]
    color_index = colors.index(tuple(settings["snake_color"])) if tuple(settings["snake_color"]) in colors else 0

    running = True
    while running:
        screen.fill(LIGHT_BLUE)

        title = font.render("SETTINGS", True, (0, 0, 0))

        grid_text = small_font.render(f"Grid: {'ON' if settings['grid_overlay'] else 'OFF'}", True, (0, 0, 0))
        color_text = small_font.render("Snake Color:", True, (0, 0, 0))
        hint_text = small_font.render("G - Grid | C - Color | ESC - Save & Back", True, (100, 100, 100))

        # Draw color preview box
        pygame.draw.rect(screen, colors[color_index], (200, 300, 100, 50))

        screen.blit(title, (200, 100))
        screen.blit(grid_text, (200, 200))
        screen.blit(color_text, (200, 250))
        screen.blit(hint_text, (50, 500))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings(settings)
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    settings["grid_overlay"] = not settings["grid_overlay"]

                elif event.key == pygame.K_c:
                    color_index = (color_index + 1) % len(colors)
                    settings["snake_color"] = list(colors[color_index])

                elif event.key == pygame.K_ESCAPE:
                    save_settings(settings)
                    return
    
# Main state controller
state = "MENU"
current_user = ""

#game will work all the time 
while True:
    if state == "MENU":
        res = main_menu()
        if not res: break
        state, current_user = res
    elif state == "GAME":
        res = play_game(current_user)
        if res == "MENU": state = "MENU"
        else:
            # Simple game over logic
            state = "MENU" # Or implement a specific GameOver screen loop
    elif state == "LEADER":
        show_leaderboard()
        state = "MENU"
    elif state == "SETTINGS":
        settings_screen(screen)
        state = "MENU"

pygame.quit()