import pygame, sys
from pygame.locals import *
import random
import time
 
pygame.init() #initializing pygame
 
FPS = 60 #60 frames per second is a speed of display update
FramePerSec = pygame.time.Clock()
 
# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
# Screen information
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5 #variable for speed
SCORE = 0 #will be counting score
COINS = 0 #will be adding coin numbers
 
#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 40)
game_over = font.render("Game Over", True, BLACK)
 
background = pygame.image.load("AnimatedStreet.jpg")
 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
 
 
class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("enemy_car.png") #changed name for my images
        self.image = pygame.transform.scale(self.image, (60, 100)) #changing the size
        self.rect = self.image.get_rect() #this rectangle will represent physical properties of a car
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),0) #random appereance of the enemy car
 
      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED) #movement of the car by pixels
        if (self.rect.bottom > 600):
            SCORE += 1 #adding the score
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0) 
 
      def draw(self, surface):
        surface.blit(self.image, self.rect) #drawing the image from the start in specific rectangle every loop iteration
 
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("my_car.png") #changed name for my images
        self.image = pygame.transform.scale(self.image, (60, 100)) #changing the size
        self.rect = self.image.get_rect() #this rectangle will represent physical properties of a car
        self.rect.center = (160, 520) #exact appereance of the player car
 
    def move(self):
        pressed_keys = pygame.key.get_pressed()
       #if pressed_keys[K_UP]:
            #self.rect.move_ip(0, -5)
       #if pressed_keys[K_DOWN]:
            #self.rect.move_ip(0,5)
         
        if self.rect.left > 0: #starting from left so that we can check if my car will not get out from the display
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
 
    def draw(self, surface):
        surface.blit(self.image, self.rect)     
        
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.respawn()

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.respawn()

    def respawn(self):
        self.rect.center = (
            random.randint(30, SCREEN_WIDTH - 30),
            random.randint(-100, -40)
        )
 
         
P1 = Player()
E1 = Enemy()
C = Coin()
 
#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C)

#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 60000)


while True:     
    #Cycles through all events occuring  
    for event in pygame.event.get(): #event speed of the game increases
        if event.type == INC_SPEED:
              SPEED += 2
           
        if event.type == QUIT: 
            pygame.quit()
            sys.exit()
     
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, WHITE)
    DISPLAYSURF.blit(scores, (10,10))
    
    coin_text = font_small.render(f"Coins: {COINS}", True, WHITE)
    DISPLAYSURF.blit(coin_text, (10, 40))

    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
         
         
    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound('crash.mpeg').play()
          time.sleep(0.5)
                    
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
           
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()     
          
    # Collision with coin
    collected = pygame.sprite.spritecollide(P1, coins, False)
    for coin in collected:
        COINS += 1
        coin.respawn()  
          
    pygame.display.update()
    FramePerSec.tick(FPS)