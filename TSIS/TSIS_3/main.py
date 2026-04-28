import pygame, sys
from pygame.locals import *
from persistence import load_settings, save_settings, load_leaderboard, add_score
from ui import draw_button, clicked
from racer import run_game

pygame.init()
SCREEN_W, SCREEN_H = 400, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()

font_big = pygame.font.SysFont("Verdana", 48, bold=True)
font_med = pygame.font.SysFont("Verdana", 30)
font_sml = pygame.font.SysFont("Verdana", 20)

WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
YELLOW = (255, 220, 0)
GRAY   = (180, 180, 180)

# Background colors
bg_map = {
    "dark": (20, 20, 40),
    "gray": (60, 60, 60),
    "light": (200, 200, 200)
}


# ── Screens ─────────────────────────────────────────────────────────

def menu_screen(settings):
    while True:
        clock.tick(60)
        screen.fill(bg_map.get(settings.get("bg_color", "dark")))

        t = font_big.render("RACER", True, YELLOW)
        screen.blit(t, t.get_rect(center=(200, 90)))

        play_btn = pygame.Rect(130, 180, 140, 50)
        lb_btn   = pygame.Rect(100, 250, 200, 50)
        set_btn  = pygame.Rect(130, 320, 140, 50)
        quit_btn = pygame.Rect(130, 390, 140, 50)

        draw_button(screen, "Play",        play_btn, font_med)
        draw_button(screen, "Leaderboard", lb_btn,   font_sml)
        draw_button(screen, "Settings",    set_btn,  font_med)
        draw_button(screen, "Quit",        quit_btn, font_med)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if clicked(play_btn, event): return "USERNAME"
            if clicked(lb_btn,   event): return "LEADERBOARD"
            if clicked(set_btn,  event): return "SETTINGS"
            if clicked(quit_btn, event):
                pygame.quit(); sys.exit()


def username_screen(settings):
    name = ""
    while True:
        clock.tick(60)
        screen.fill(bg_map.get(settings.get("bg_color", "dark")))

        lbl = font_med.render("Enter Your Name:", True, WHITE)
        screen.blit(lbl, lbl.get_rect(center=(200, 200)))

        name_surf = font_big.render((name or " ") + "_", True, YELLOW)
        screen.blit(name_surf, name_surf.get_rect(center=(200, 300)))

        hint = font_sml.render("Press ENTER to start", True, GRAY)
        screen.blit(hint, hint.get_rect(center=(200, 390)))

        back_btn = pygame.Rect(140, 450, 120, 40)
        draw_button(screen, "Back", back_btn, font_sml)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if clicked(back_btn, event):
                return "MENU", ""
            if event.type == KEYDOWN:
                if event.key == K_RETURN and name.strip():
                    return "GAME", name.strip()
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                elif event.unicode.isprintable() and len(name) < 15:
                    name += event.unicode


def gameover_screen(settings, username, score, distance, coins):
    while True:
        clock.tick(60)
        screen.fill((70, 0, 0))

        t = font_big.render("GAME OVER", True, WHITE)
        screen.blit(t, t.get_rect(center=(200, 80)))

        for i, line in enumerate([
            f"Player:   {username}",
            f"Score:    {score}",
            f"Distance: {distance:.1f} m",
            f"Coins:    {coins}",
        ]):
            txt = font_sml.render(line, True, WHITE)
            screen.blit(txt, txt.get_rect(center=(200, 200 + i * 45)))

        retry_btn = pygame.Rect(60,  430, 120, 50)
        menu_btn  = pygame.Rect(220, 430, 120, 50)
        draw_button(screen, "Retry", retry_btn, font_med)
        draw_button(screen, "Menu",  menu_btn,  font_med)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if clicked(retry_btn, event): return "GAME"
            if clicked(menu_btn,  event): return "MENU"


def leaderboard_screen(settings):
    lb = load_leaderboard()
    while True:
        clock.tick(60)
        screen.fill(bg_map.get(settings.get("bg_color", "dark")))

        t = font_med.render("TOP 10 SCORES", True, YELLOW)
        screen.blit(t, t.get_rect(center=(200, 30)))

        headers = font_sml.render(" # Name      Score   Dist", True, GRAY)
        screen.blit(headers, (10, 65))
        pygame.draw.line(screen, GRAY, (10, 85), (390, 85), 1)

        for i, e in enumerate(lb[:10]):
            txt = f"{i+1:2}. {e['name'][:12]:<12}  {e['score']:>5}   {e['distance']}m"
            col = YELLOW if i == 0 else WHITE
            screen.blit(font_sml.render(txt, True, col), (10, 92 + i * 44))

        back_btn = pygame.Rect(140, 555, 120, 38)
        draw_button(screen, "Back", back_btn, font_med)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if clicked(back_btn, event): return "MENU"


def settings_screen(settings):
    s = settings.copy()

    while True:
        clock.tick(60)
        screen.fill(bg_map.get(s.get("bg_color", "dark")))

        screen.blit(font_med.render("SETTINGS", True, YELLOW),
                    font_med.render("SETTINGS", True, YELLOW).get_rect(center=(200, 40)))

        # Sound
        screen.blit(font_sml.render("Sound:", True, WHITE), (40, 120))
        sound_btn = pygame.Rect(200, 112, 100, 36)
        draw_button(screen, "ON" if s["sound"] else "OFF", sound_btn, font_sml,
                    color=(0,160,0) if s["sound"] else (160,0,0),
                    text_color=WHITE)

        # Background color
        screen.blit(font_sml.render("Background:", True, WHITE), (40, 185))
        bg_colors = {
            "dark": (20, 20, 40),
            "gray": (60, 60, 60),
            "light": (200, 200, 200)
        }

        bg_btns = []
        for i, (name, col) in enumerate(bg_colors.items()):
            cb = pygame.Rect(130 + i * 90, 177, 80, 36)
            draw_button(screen, name.capitalize(), cb, font_sml,
                        color=col,
                        text_color=BLACK if name == "light" else WHITE)

            if s.get("bg_color") == name:
                pygame.draw.rect(screen, YELLOW, cb, 3, border_radius=6)

            bg_btns.append((cb, name))

        back_btn = pygame.Rect(130, 520, 140, 44)
        draw_button(screen, "Save & Back", back_btn, font_sml)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if clicked(sound_btn, event):
                s["sound"] = not s["sound"]
            for btn, name in bg_btns:
                if clicked(btn, event):
                    s["bg_color"] = name
            if clicked(back_btn, event):
                save_settings(s)
                return "MENU", s


# ── Main ───────────────────────────────────────────────────────────

def main():
    settings = load_settings()
    state    = "MENU"
    username = ""
    last     = (0, 0, 0)

    while True:
        if state == "MENU":
            state = menu_screen(settings)

        elif state == "USERNAME":
            state, username = username_screen(settings)

        elif state == "GAME":
            last  = run_game(screen, settings, username)
            add_score(username, last[0], last[1])
            state = "GAMEOVER"

        elif state == "GAMEOVER":
            state = gameover_screen(settings, username, *last)

        elif state == "LEADERBOARD":
            state = leaderboard_screen(settings)

        elif state == "SETTINGS":
            state, settings = settings_screen(settings)


if __name__ == "__main__":
    main()