import pygame

pygame.init()

WIDTH = 400
HEIGHT = 300

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

clock = pygame.time.Clock()

done = False

radius = 25
x = WIDTH // 2
y = HEIGHT // 2

while not done:

    screen.fill((255, 255, 255))  # white background

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:

            # move 20 pixels each press
            if event.key == pygame.K_UP:
                if y - 20 - radius >= 0:
                    y -= 20

            if event.key == pygame.K_DOWN:
                if y + 20 + radius <= HEIGHT:
                    y += 20

            if event.key == pygame.K_LEFT:
                if x - 20 - radius >= 0:
                    x -= 20

            if event.key == pygame.K_RIGHT:
                if x + 20 + radius <= WIDTH:
                    x += 20

    pygame.draw.circle(screen, (255, 0, 0), (x, y), radius)

    pygame.display.flip()
    clock.tick(20)

pygame.quit()