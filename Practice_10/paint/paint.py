import pygame

pygame.init()

# --- SETTINGS ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()
fps = 60

# --- COLORS ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

colors = [
    (0, 0, 255), (255, 0, 0), (0, 255, 0),
    (255, 255, 0), (0, 255, 255),
    (255, 0, 255), (0, 0, 0)
]

# --- STATE ---
active_color = BLACK
active_shape = "circle"   # circle / rect / eraser
drawing = False
start_pos = (0, 0)

canvas = []  # storage for shapes


# --- MENU ---
def draw_menu():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 70))

    circle_btn = pygame.draw.rect(screen, BLACK, (10, 10, 50, 50), 2)
    rect_btn = pygame.draw.rect(screen, BLACK, (70, 10, 50, 50), 2)
    eraser_btn = pygame.draw.rect(screen, BLACK, (130, 10, 50, 50), 2)

    pygame.draw.circle(screen, BLACK, (35, 35), 15, 2)
    pygame.draw.rect(screen, BLACK, (85, 20, 30, 30), 2)
    pygame.draw.rect(screen, WHITE, (140, 20, 30, 30))

    color_rects = []
    x = WIDTH - 250

    for col in colors:
        rect = pygame.draw.rect(screen, col, (x, 15, 25, 25))
        color_rects.append((rect, col))
        x += 30

    return circle_btn, rect_btn, eraser_btn, color_rects


# --- DRAW SHAPES ---
def draw_canvas():
    for shape in canvas:
        if shape["type"] == "circle":
            pygame.draw.circle(screen, shape["color"], shape["pos"], shape["radius"], 2)

        elif shape["type"] == "rect":
            pygame.draw.rect(screen, shape["color"], shape["rect"], 2)


# --- GAME LOOP ---
run = True
while run:
    clock.tick(fps)
    screen.fill(WHITE)

    mouse = pygame.mouse.get_pos()

    # menu
    circle_btn, rect_btn, eraser_btn, color_rects = draw_menu()

    # draw saved shapes
    draw_canvas()

    # preview drawing
    if drawing:
        if active_shape == "circle":
            radius = int(((mouse[0]-start_pos[0])**2 + (mouse[1]-start_pos[1])**2) ** 0.5)
            pygame.draw.circle(screen, active_color, start_pos, radius, 2)

        elif active_shape == "rect":
            rect = pygame.Rect(start_pos, (mouse[0]-start_pos[0], mouse[1]-start_pos[1]))
            pygame.draw.rect(screen, active_color, rect, 2)

    # --- EVENTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse[1] < 70:
                # tools
                if circle_btn.collidepoint(mouse):
                    active_shape = "circle"
                elif rect_btn.collidepoint(mouse):
                    active_shape = "rect"
                elif eraser_btn.collidepoint(mouse):
                    active_shape = "eraser"

                # colors
                for rect, col in color_rects:
                    if rect.collidepoint(mouse):
                        active_color = col
                        active_shape = "circle"

            else:
                drawing = True
                start_pos = mouse

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                drawing = False

                if active_shape == "circle":
                    radius = int(((mouse[0]-start_pos[0])**2 + (mouse[1]-start_pos[1])**2) ** 0.5)
                    canvas.append({
                        "type": "circle",
                        "color": active_color,
                        "pos": start_pos,
                        "radius": radius
                    })

                elif active_shape == "rect":
                    rect = pygame.Rect(start_pos, (mouse[0]-start_pos[0], mouse[1]-start_pos[1]))
                    canvas.append({
                        "type": "rect",
                        "color": active_color,
                        "rect": rect
                    })

        # --- ERASER ---
        if pygame.mouse.get_pressed()[0] and active_shape == "eraser":
            new_canvas = []

            for shape in canvas:

                if shape["type"] == "rect":
                    rect = shape["rect"]

                elif shape["type"] == "circle":
                    rect = pygame.Rect(
                        shape["pos"][0] - shape["radius"],
                        shape["pos"][1] - shape["radius"],
                        shape["radius"] * 2,
                        shape["radius"] * 2
                    )

                if not rect.collidepoint(mouse):
                    new_canvas.append(shape)

            canvas = new_canvas

    pygame.display.flip()

pygame.quit()