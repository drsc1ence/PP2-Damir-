import pygame
import os

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((600,300))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont("Arial",30)
small_font = pygame.font.SysFont("Arial",22)

playlist = [
    "music/song1.mp3",
    "music/song2.mp3"
]

current_track = 0
playing = False

def play_track(index):
    global playing
    pygame.mixer.music.load(playlist[index])
    pygame.mixer.music.play()
    playing = True

def draw_ui():

    screen.fill((30,30,30))

    track = os.path.basename(playlist[current_track])

    track_text = font.render("Track: " + track, True, (255,255,255))
    screen.blit(track_text,(40,60))

    status = "Playing" if playing else "Stopped"
    status_text = font.render("Status: " + status, True,(200,200,200))
    screen.blit(status_text,(40,120))

    pos = pygame.mixer.music.get_pos() // 1000
    time_text = small_font.render(f"Position: {pos} sec",True,(180,180,180))
    screen.blit(time_text,(40,180))

    help_text = small_font.render("P=Play  S=Stop  N=Next  B=Back  Q=Quit",True,(150,150,150))
    screen.blit(help_text,(40,240))

    pygame.display.update()

running = True
clock = pygame.time.Clock()

while running:

    draw_ui()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:
                play_track(current_track)

            elif event.key == pygame.K_s:
                pygame.mixer.music.stop()
                playing = False

            elif event.key == pygame.K_n:
                current_track = (current_track + 1) % len(playlist)
                play_track(current_track)

            elif event.key == pygame.K_b:
                current_track = (current_track - 1) % len(playlist)
                play_track(current_track)

            elif event.key == pygame.K_q:
                running = False

    clock.tick(30)

pygame.quit()