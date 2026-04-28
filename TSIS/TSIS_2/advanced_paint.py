import pygame
import datetime

pygame.init()

# --- SETTINGS ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint - Advanced Drawing Tool")

clock = pygame.time.Clock()
fps = 60

# --- COLORS ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)

colors = [
    (0, 0, 255), (255, 0, 0), (0, 255, 0),
    (255, 255, 0), (0, 255, 255), (255, 0, 255), BLACK
]

# --- STATE ---
active_color = BLACK
active_tool = "circle"   # circle, rect, square, r_triangle, eq_triangle, rhombus, pencil, line, eraser, fill, text
brush_size = 2  # 2, 5, 10

drawing = False
start_pos = (0, 0)
last_pos = None  # for continuous drawing (pencil, eraser)

# Text input state
text_input_active = False
text_pos = (0, 0)
text_string = ""
text_font = pygame.font.SysFont("Arial", 24)

# Create main canvas surface
canvas_surface = pygame.Surface((WIDTH, HEIGHT))
canvas_surface.fill(WHITE)

# --- MENU FUNCTIONS ---
def draw_menu():
    """Draw toolbar and return button rectangles for interactive elements"""
    # Draw toolbar background (two rows)
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 100))
    pygame.draw.line(screen, BLACK, (0, 70), (WIDTH, 70), 2)
    
    # First row (y=10 to 60) - Shape tools
    circle_btn = pygame.draw.rect(screen, LIGHT_GRAY, (10, 10, 50, 50), 2)
    rect_btn = pygame.draw.rect(screen, LIGHT_GRAY, (70, 10, 50, 50), 2)
    sq_btn = pygame.draw.rect(screen, LIGHT_GRAY, (130, 10, 50, 50), 2)
    r_tr_btn = pygame.draw.rect(screen, LIGHT_GRAY, (190, 10, 50, 50), 2)
    eq_tr_btn = pygame.draw.rect(screen, LIGHT_GRAY, (250, 10, 50, 50), 2)
    rh_btn = pygame.draw.rect(screen, LIGHT_GRAY, (310, 10, 50, 50), 2)
    eraser_btn = pygame.draw.rect(screen, LIGHT_GRAY, (370, 10, 50, 50), 2)
    
    # Draw icons for first row
    pygame.draw.circle(screen, BLACK, (35, 35), 15, 2)
    pygame.draw.rect(screen, BLACK, (80, 25, 30, 20), 2)
    pygame.draw.rect(screen, BLACK, (140, 20, 30, 30), 2)
    pygame.draw.polygon(screen, BLACK, [(200, 15), (200, 50), (235, 50)], 2)
    pygame.draw.polygon(screen, BLACK, [(275, 20), (255, 50), (295, 50)], 2)
    pygame.draw.polygon(screen, BLACK, [(335, 20), (355, 35), (335, 50), (315, 35)], 2)
    pygame.draw.rect(screen, WHITE, (380, 20, 30, 30))  # eraser icon
    
    # Second row (y=75 to 125) - New tools
    pencil_btn = pygame.draw.rect(screen, LIGHT_GRAY, (10, 75, 50, 20), 2)
    line_btn = pygame.draw.rect(screen, LIGHT_GRAY, (70, 75, 50, 20), 2)
    fill_btn = pygame.draw.rect(screen, LIGHT_GRAY, (130, 75, 50, 20), 2)
    text_btn = pygame.draw.rect(screen, LIGHT_GRAY, (190, 75, 50, 20), 2)
    
    # Brush size buttons
    small_btn = pygame.draw.rect(screen, LIGHT_GRAY, (260, 75, 40, 20), 2)
    medium_btn = pygame.draw.rect(screen, LIGHT_GRAY, (310, 75, 40, 20), 2)
    large_btn = pygame.draw.rect(screen, LIGHT_GRAY, (360, 75, 40, 20), 2)
    
    # Draw text on buttons
    small_font = pygame.font.SysFont("Arial", 12)
    screen.blit(small_font.render("S", True, BLACK), (275, 78))
    screen.blit(small_font.render("M", True, BLACK), (325, 78))
    screen.blit(small_font.render("L", True, BLACK), (375, 78))
    
    # Draw tool labels
    screen.blit(small_font.render("Pencil", True, BLACK), (15, 78))
    screen.blit(small_font.render("Line", True, BLACK), (75, 78))
    screen.blit(small_font.render("Fill", True, BLACK), (140, 78))
    screen.blit(small_font.render("Text", True, BLACK), (195, 78))
    
    # Display current brush size
    size_text = small_font.render(f"Size: {brush_size}", True, BLACK)
    screen.blit(size_text, (420, 78))
    
    # Color palette (top right)
    color_rects = []
    x = WIDTH - 250
    y = 10
    for col in colors:
        rect = pygame.draw.rect(screen, col, (x, y, 25, 25))
        if col == active_color:
            pygame.draw.rect(screen, BLACK, (x-2, y-2, 29, 29), 2)
        color_rects.append((rect, col))
        x += 30
        
    # Highlight active tool
    if active_tool == "circle":
        pygame.draw.rect(screen, BLACK, (10, 10, 50, 50), 3)
    elif active_tool == "rect":
        pygame.draw.rect(screen, BLACK, (70, 10, 50, 50), 3)
    elif active_tool == "square":
        pygame.draw.rect(screen, BLACK, (130, 10, 50, 50), 3)
    elif active_tool == "r_triangle":
        pygame.draw.rect(screen, BLACK, (190, 10, 50, 50), 3)
    elif active_tool == "eq_triangle":
        pygame.draw.rect(screen, BLACK, (250, 10, 50, 50), 3)
    elif active_tool == "rhombus":
        pygame.draw.rect(screen, BLACK, (310, 10, 50, 50), 3)
    elif active_tool == "eraser":
        pygame.draw.rect(screen, BLACK, (370, 10, 50, 50), 3)
    elif active_tool == "pencil":
        pygame.draw.rect(screen, BLACK, (10, 75, 50, 20), 3)
    elif active_tool == "line":
        pygame.draw.rect(screen, BLACK, (70, 75, 50, 20), 3)
    elif active_tool == "fill":
        pygame.draw.rect(screen, BLACK, (130, 75, 50, 20), 3)
    elif active_tool == "text":
        pygame.draw.rect(screen, BLACK, (190, 75, 50, 20), 3)
    
    return (circle_btn, rect_btn, sq_btn, r_tr_btn, eq_tr_btn, rh_btn, eraser_btn,
            pencil_btn, line_btn, fill_btn, text_btn,
            small_btn, medium_btn, large_btn, color_rects)

# --- FLOOD FILL IMPLEMENTATION ---
def flood_fill(surface, x, y, target_color, replacement_color):
    """Flood fill algorithm using stack (non-recursive)"""
    if target_color == replacement_color:
        return
    
    stack = [(x, y)]
    width, height = surface.get_size()
    
    while stack:
        px, py = stack.pop()
        
        # Check bounds
        if px < 0 or px >= width or py < 0 or py >= height:
            continue
            
        # Get current pixel color
        try:
            current_color = surface.get_at((px, py))
        except:
            continue
            
        # Compare colors (exact match)
        if current_color != target_color:
            continue
            
        # Set new color
        surface.set_at((px, py), replacement_color)
        
        # Add neighbors
        stack.append((px + 1, py))
        stack.append((px - 1, py))
        stack.append((px, py + 1))
        stack.append((px, py - 1))

# --- TEXT TOOL FUNCTIONS ---
def render_text_on_canvas(surface, pos, text, color):
    """Render text onto canvas surface"""
    text_surface = text_font.render(text, True, color)
    surface.blit(text_surface, pos)

# --- GAME LOOP ---
run = True
while run:
    clock.tick(fps)
    
    # Draw canvas
    screen.blit(canvas_surface, (0, 0))
    
    # Draw toolbar
    (circle_btn, rect_btn, sq_btn, r_tr_btn, eq_tr_btn, rh_btn, eraser_btn,
     pencil_btn, line_btn, fill_btn, text_btn,
     small_btn, medium_btn, large_btn, color_rects) = draw_menu()
    
    # Get mouse position
    mouse = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    
    # Handle pencil and eraser continuous drawing
    if mouse_pressed[0] and not text_input_active:
        if active_tool == "pencil" and mouse[1] > 100:
            if last_pos is not None:
                pygame.draw.line(canvas_surface, active_color, last_pos, mouse, brush_size)
            last_pos = mouse
        elif active_tool == "eraser" and mouse[1] > 100:
            if last_pos is not None:
                pygame.draw.line(canvas_surface, WHITE, last_pos, mouse, brush_size)
            last_pos = mouse
        else:
            last_pos = None
            
        # Update last_pos for pencil/eraser
        if active_tool in ["pencil", "eraser"] and mouse[1] > 100:
            last_pos = mouse
    
    # Preview for shape/line drawing
    if drawing and not text_input_active:
        if active_tool == "line":
            # Preview line
            pygame.draw.line(screen, active_color, start_pos, mouse, brush_size)
        elif active_tool == "circle":
            radius = int(((mouse[0]-start_pos[0])**2 + (mouse[1]-start_pos[1])**2) ** 0.5)
            pygame.draw.circle(screen, active_color, start_pos, radius, brush_size)
        elif active_tool == "rect":
            rect = pygame.Rect(start_pos, (mouse[0]-start_pos[0], mouse[1]-start_pos[1]))
            pygame.draw.rect(screen, active_color, rect, brush_size)
        elif active_tool == "square":
            size = max(abs(mouse[0]-start_pos[0]), abs(mouse[1]-start_pos[1]))
            rect = pygame.Rect(start_pos[0], start_pos[1], size, size)
            pygame.draw.rect(screen, active_color, rect, brush_size)
        elif active_tool == "r_triangle":
            points = [start_pos, (start_pos[0], mouse[1]), mouse]
            pygame.draw.polygon(screen, active_color, points, brush_size)
        elif active_tool == "eq_triangle":
            x1, y1 = start_pos
            x2, y2 = mouse
            width = x2 - x1
            points = [(x1 + width // 2, y1), (x1, y2), (x2, y2)]
            pygame.draw.polygon(screen, active_color, points, brush_size)
        elif active_tool == "rhombus":
            x1, y1 = start_pos
            x2, y2 = mouse
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
            pygame.draw.polygon(screen, active_color, points, brush_size)
    
    # Display text input preview
    if text_input_active:
        # Draw cursor
        cursor_pos = (text_pos[0] + text_font.size(text_string)[0], text_pos[1])
        pygame.draw.line(screen, BLACK, cursor_pos, (cursor_pos[0], cursor_pos[1] + 20), 2)
        # Draw current text string
        if text_string:
            temp_surface = text_font.render(text_string, True, active_color)
            screen.blit(temp_surface, text_pos)
    
    # --- EVENTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        # Keyboard shortcuts
        if event.type == pygame.KEYDOWN:
            # Brush size shortcuts (1,2,3)
            if event.key == pygame.K_1:
                brush_size = 2
            elif event.key == pygame.K_2:
                brush_size = 5
            elif event.key == pygame.K_3:
                brush_size = 10
                
            # Save shortcut (Ctrl+S)
            if event.mod & pygame.KMOD_CTRL and event.key == pygame.K_s:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"canvas_{timestamp}.png"
                pygame.image.save(canvas_surface, filename)
                print(f"Canvas saved as {filename}")
            
            # Text input handling
            if text_input_active:
                if event.key == pygame.K_RETURN:
                    # Commit text to canvas
                    render_text_on_canvas(canvas_surface, text_pos, text_string, active_color)
                    text_input_active = False
                    text_string = ""
                elif event.key == pygame.K_ESCAPE:
                    # Cancel text input
                    text_input_active = False
                    text_string = ""
                elif event.key == pygame.K_BACKSPACE:
                    text_string = text_string[:-1]
                else:
                    # Add character (only printable characters)
                    if event.unicode and event.unicode.isprintable():
                        text_string += event.unicode
        
        # Mouse button down
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse[1] < 100:
                # Tool selection in toolbar
                if circle_btn.collidepoint(mouse):
                    active_tool = "circle"
                    text_input_active = False
                elif rect_btn.collidepoint(mouse):
                    active_tool = "rect"
                    text_input_active = False
                elif sq_btn.collidepoint(mouse):
                    active_tool = "square"
                    text_input_active = False
                elif r_tr_btn.collidepoint(mouse):
                    active_tool = "r_triangle"
                    text_input_active = False
                elif eq_tr_btn.collidepoint(mouse):
                    active_tool = "eq_triangle"
                    text_input_active = False
                elif rh_btn.collidepoint(mouse):
                    active_tool = "rhombus"
                    text_input_active = False
                elif eraser_btn.collidepoint(mouse):
                    active_tool = "eraser"
                    text_input_active = False
                elif pencil_btn.collidepoint(mouse):
                    active_tool = "pencil"
                    text_input_active = False
                elif line_btn.collidepoint(mouse):
                    active_tool = "line"
                    text_input_active = False
                elif fill_btn.collidepoint(mouse):
                    active_tool = "fill"
                    text_input_active = False
                elif text_btn.collidepoint(mouse):
                    active_tool = "text"
                    text_input_active = False
                # Brush size buttons
                elif small_btn.collidepoint(mouse):
                    brush_size = 2
                elif medium_btn.collidepoint(mouse):
                    brush_size = 5
                elif large_btn.collidepoint(mouse):
                    brush_size = 10
                # Color selection
                for rect, col in color_rects:
                    if rect.collidepoint(mouse):
                        active_color = col
            else:
                # Canvas area clicks
                if active_tool == "fill" and not text_input_active:
                    # Perform flood fill
                    target_color = canvas_surface.get_at(mouse)
                    flood_fill(canvas_surface, mouse[0], mouse[1], target_color, active_color)
                elif active_tool == "text":
                    # Start text input at click position
                    text_input_active = True
                    text_pos = mouse
                    text_string = ""
                elif active_tool in ["line", "circle", "rect", "square", "r_triangle", "eq_triangle", "rhombus"]:
                    drawing = True
                    start_pos = mouse
                elif active_tool in ["pencil", "eraser"]:
                    last_pos = mouse
        
        # Mouse button up
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and not text_input_active:
                final_pos = mouse
                
                if active_tool == "line":
                    # Draw line on canvas
                    pygame.draw.line(canvas_surface, active_color, start_pos, final_pos, brush_size)
                elif active_tool == "circle":
                    radius = int(((final_pos[0]-start_pos[0])**2 + (final_pos[1]-start_pos[1])**2) ** 0.5)
                    pygame.draw.circle(canvas_surface, active_color, start_pos, radius, brush_size)
                elif active_tool == "rect":
                    rect = pygame.Rect(start_pos, (final_pos[0]-start_pos[0], final_pos[1]-start_pos[1]))
                    pygame.draw.rect(canvas_surface, active_color, rect, brush_size)
                elif active_tool == "square":
                    size = max(abs(final_pos[0]-start_pos[0]), abs(final_pos[1]-start_pos[1]))
                    rect = pygame.Rect(start_pos[0], start_pos[1], size, size)
                    pygame.draw.rect(canvas_surface, active_color, rect, brush_size)
                elif active_tool == "r_triangle":
                    points = [start_pos, (start_pos[0], final_pos[1]), final_pos]
                    pygame.draw.polygon(canvas_surface, active_color, points, brush_size)
                elif active_tool == "eq_triangle":
                    x1, y1 = start_pos
                    x2, y2 = final_pos
                    width = x2 - x1
                    points = [(x1 + width // 2, y1), (x1, y2), (x2, y2)]
                    pygame.draw.polygon(canvas_surface, active_color, points, brush_size)
                elif active_tool == "rhombus":
                    x1, y1 = start_pos
                    x2, y2 = final_pos
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
                    pygame.draw.polygon(canvas_surface, active_color, points, brush_size)
                
                drawing = False
        
        # Mouse motion for continuous drawing (already handled above)
    
    pygame.display.flip()

pygame.quit()