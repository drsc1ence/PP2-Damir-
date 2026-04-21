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
    sq_btn = pygame.draw.rect(screen, BLACK, (130, 10, 50, 50), 2)
    r_tr_btn = pygame.draw.rect(screen, BLACK, (190, 10, 50, 50), 2)
    eq_tr_btn = pygame.draw.rect(screen, BLACK, (250, 10, 50, 50), 2)
    rh_btn = pygame.draw.rect(screen, BLACK, (310, 10, 50, 50), 2)
    eraser_btn = pygame.draw.rect(screen, BLACK, (370, 10, 50, 50), 2)

    pygame.draw.circle(screen, BLACK, (35, 35), 15, 2)
    pygame.draw.rect(screen, BLACK, (80, 25, 30, 20), 2)
    pygame.draw.rect(screen, BLACK, (140, 20, 30, 30), 2)
    pygame.draw.polygon(screen, BLACK, [(200, 15), (200, 50), (235, 50)], 2)
    pygame.draw.polygon(screen, BLACK, [(275, 20), (255, 50), (295, 50)], 2)
    pygame.draw.polygon(screen, BLACK, [(335, 20), (355, 35), (335, 50), (315, 35)], 2)
    pygame.draw.rect(screen, WHITE, (380, 20, 30, 30))

    color_rects = []
    x = WIDTH - 250

    for col in colors:
        rect = pygame.draw.rect(screen, col, (x, 15, 25, 25))
        color_rects.append((rect, col))
        x += 30

    return circle_btn, rect_btn, sq_btn, r_tr_btn, eq_tr_btn, rh_btn, eraser_btn, color_rects


# --- DRAW SHAPES ---
def draw_canvas():
    for shape in canvas:
        if shape["type"] == "circle":
            pygame.draw.circle(screen, shape["color"], shape["pos"], shape["radius"], 2)

        elif shape["type"] == "rect":
            pygame.draw.rect(screen, shape["color"], shape["rect"], 2)
        
        elif shape["type"] == "square":
            pygame.draw.rect(screen, shape["color"], shape["rect"], 2)

        elif shape["type"] in ["r_triangle", "eq_triangle", "rhombus"]:
            pygame.draw.polygon(screen, shape["color"], shape["points"], 2)


# --- GAME LOOP ---
run = True
while run:
    clock.tick(fps)
    screen.fill(WHITE)

    mouse = pygame.mouse.get_pos()

    # menu
    circle_btn, rect_btn, sq_btn, r_tr_btn, eq_tr_btn, rh_btn, eraser_btn, color_rects = draw_menu()

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
            
        elif active_shape == "square":
            size = max(abs(mouse[0]-start_pos[0]), abs(mouse[1]-start_pos[1]))
            rect = pygame.Rect(start_pos[0], start_pos[1], size, size)
            pygame.draw.rect(screen, active_color, rect, 2)

        elif active_shape == "r_triangle":
            pygame.draw.polygon(screen, active_color, [
                start_pos,
                (start_pos[0], mouse[1]),
                mouse
            ], 2)

        elif active_shape == "eq_triangle":
            x1, y1 = start_pos
            x2, y2 = mouse
            width = x2 - x1
            points = [
                (x1 + width // 2, y1),
                (x1, y2),
                (x2, y2)
            ]
            pygame.draw.polygon(screen, active_color, points, 2)

        elif active_shape == "rhombus":
            x1, y1 = start_pos
            x2, y2 = mouse
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            points = [
                (cx, y1),
                (x2, cy),
                (cx, y2),
                (x1, cy)
            ]
            pygame.draw.polygon(screen, active_color, points, 2)

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
                elif sq_btn.collidepoint(mouse):
                    active_shape = "square"
                elif r_tr_btn.collidepoint(mouse):
                    active_shape = "r_triangle"
                elif eq_tr_btn.collidepoint(mouse):
                    active_shape = "eq_triangle"
                elif rh_btn.collidepoint(mouse):
                    active_shape = "rhombus"
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
                
                elif active_shape == "square":
                    size = max(abs(mouse[0]-start_pos[0]), abs(mouse[1]-start_pos[1]))
                    rect = pygame.Rect(start_pos[0], start_pos[1], size, size)

                    canvas.append({
                        "type": "square",
                        "color": active_color,
                        "rect": rect
                    })

                elif active_shape == "r_triangle":
                    points = [
                        start_pos,
                        (start_pos[0], mouse[1]),
                        mouse
                    ]

                    canvas.append({
                        "type": "r_triangle",
                        "color": active_color,
                        "points": points
                    })

                elif active_shape == "eq_triangle":
                    x1, y1 = start_pos
                    x2, y2 = mouse
                    width = x2 - x1

                    points = [
                        (x1 + width // 2, y1),
                        (x1, y2),
                        (x2, y2)
                    ]

                    canvas.append({
                        "type": "eq_triangle",
                        "color": active_color,
                        "points": points
                    })

                elif active_shape == "rhombus":
                    x1, y1 = start_pos
                    x2, y2 = mouse
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2

                    points = [
                        (cx, y1),
                        (x2, cy),
                        (cx, y2),
                        (x1, cy)
                    ]

                    canvas.append({
                        "type": "rhombus",
                        "color": active_color,
                        "points": points
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
                    
                elif shape["type"] in ["r_triangle", "eq_triangle", "rhombus"]:
                    xs = [p[0] for p in shape["points"]]
                    ys = [p[1] for p in shape["points"]]
                    rect = pygame.Rect(min(xs), min(ys), max(xs)-min(xs), max(ys)-min(ys))

                if not rect.collidepoint(mouse):
                    new_canvas.append(shape)

            canvas = new_canvas

    pygame.display.flip()

pygame.quit()