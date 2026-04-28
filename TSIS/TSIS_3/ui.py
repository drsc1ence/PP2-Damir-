import pygame

def draw_button(surface, text, rect, font, color=(80, 80, 200), text_color=(255, 255, 0)):
    pygame.draw.rect(surface, color, rect, border_radius=6)
    pygame.draw.rect(surface, (255, 255, 0), rect, 2, border_radius=6)
    lbl = font.render(text, True, text_color)
    surface.blit(lbl, lbl.get_rect(center=rect.center))

def clicked(rect, event):
    return (event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and rect.collidepoint(event.pos))
