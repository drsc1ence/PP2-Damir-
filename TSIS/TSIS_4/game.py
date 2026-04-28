import pygame
import random
import json
from config import *

class SnakeGame:
    def __init__(self, username, settings):
        self.username = username
        self.settings = settings
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = (CELL, 0)
        self.score = 0
        self.level = 1
        self.speed = 5
        self.base_speed = 5
        self.walls = []
        self.shield_active = False
        
        self.food = self.generate_pos()
        self.poison = self.generate_pos()
        self.powerup = None
        self.powerup_type = None
        self.powerup_spawn_time = 0
        self.powerup_expiry = 8000 # 8 seconds on field
        
        self.effect_end_time = 0
        self.is_slow = False

    def generate_pos(self):
        while True:
            x = random.randrange(0, WIDTH, CELL)
            y = random.randrange(0, HEIGHT, CELL)
            if (x, y) not in self.snake and (x, y) not in self.walls:
                return (x, y)

    def update_level(self):
        if self.score // 5 + 1 > self.level:
            self.level += 1
            self.base_speed += 1
            if not self.is_slow:
                self.speed = self.base_speed
            if self.level >= 3:
                self.generate_walls()

    def generate_walls(self):
        self.walls = []
        for _ in range(self.level * 2):
            w_pos = self.generate_pos()
            # Don't trap snake: ensure distance
            if abs(w_pos[0] - self.snake[0][0]) > CELL * 3:
                self.walls.append(w_pos)

    def spawn_powerup(self):
        types = ['speed', 'slow', 'shield']
        self.powerup_type = random.choice(types)
        self.powerup = self.generate_pos()
        self.powerup_spawn_time = pygame.time.get_ticks()

    def handle_powerup(self, p_type):
        now = pygame.time.get_ticks()
        if p_type == 'speed':
            self.speed = self.base_speed + 5
            self.effect_end_time = now + 5000
        elif p_type == 'slow':
            self.speed = max(2, self.base_speed - 3)
            self.is_slow = True
            self.effect_end_time = now + 5000
        elif p_type == 'shield':
            self.shield_active = True

    def move(self):
        now = pygame.time.get_ticks()
        
        # Power-up expiration on field
        if self.powerup and now - self.powerup_spawn_time > self.powerup_expiry:
            self.powerup = None

        # Power-up effect duration
        if self.effect_end_time > 0 and now > self.effect_end_time:
            self.speed = self.base_speed
            self.is_slow = False
            self.effect_end_time = 0

        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])

        # Collisions
        hit_wall = new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT
        hit_self = new_head in self.snake
        hit_obstacle = new_head in self.walls

        if hit_wall or hit_self or hit_obstacle:
            if self.shield_active:
                self.shield_active = False
                # Bounce back or skip move to stay alive
                return True
            return False

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = self.generate_pos()
            self.update_level()
            if random.random() < 0.3: self.spawn_powerup()
        elif new_head == self.poison:
            if len(self.snake) <= 3: return False
            self.snake.pop(); self.snake.pop(); self.snake.pop()
            self.poison = self.generate_pos()
        elif new_head == self.powerup:
            self.handle_powerup(self.powerup_type)
            self.powerup = None
        else:
            self.snake.pop()
            
        return True