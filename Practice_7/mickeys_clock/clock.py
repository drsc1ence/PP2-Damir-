import pygame
import math
import datetime
import os

pygame.init()
screen = pygame.display.set_mode((500, 500))
done = False
clock = pygame.time.Clock()
while not done:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        now = datetime.datetime.now()
        minutes = now.minute
        seconds = now.second
        minutes_angle = math.radians(minutes * 6)  
        seconds_angle = math.radians(seconds * 6)  
        
        hand_minutes_img = pygame.image.load('images/minutes_hand.png')
        hand_minutes_img = pygame.transform.scale(hand_minutes_img, (160, 160))
        rotated_min_img = pygame.transform.rotate(hand_minutes_img, minutes * (-6))
        
        hand_seconds_img = pygame.image.load('images/seconds_hand.png')
        hand_seconds_img = pygame.transform.scale(hand_seconds_img, (160, 160))
        rotated_sec_img = pygame.transform.rotate(hand_seconds_img, seconds * (-6))
        
                
        hand_w_min = hand_minutes_img.get_width()
        hand_w_sec = hand_seconds_img.get_width()

        img_cx_min  = 250 + (hand_w_min / 2) * math.sin(minutes_angle)
        img_cy_min  = 250 - (hand_w_min / 2) * math.cos(minutes_angle)
        
        img_cx_sec  = 250 + (hand_w_sec / 2) * math.sin(seconds_angle)
        img_cy_sec  = 250 - (hand_w_sec / 2) * math.cos(seconds_angle)
        
        screen.blit(pygame.image.load('images/clock.jpeg'), (75, 75))
        
        screen.blit(rotated_min_img, rotated_min_img.get_rect(center=(img_cx_min, img_cy_min)))     
        screen.blit(rotated_sec_img, rotated_sec_img.get_rect(center=(img_cx_sec, img_cy_sec)))        
   
        head_img = pygame.image.load('images/head.png')
        head_img = pygame.transform.scale(head_img, (120, 120))
        screen.blit(head_img, (200, 140))
        
        pygame.display.flip()
        clock.tick(60)
