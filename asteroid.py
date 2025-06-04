import pygame
import random


class Asteroid:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = random.randint(20, 50)
        self.image = pygame.image.load('./assets/img/asteroid.png')
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rotation = random.randint(0, 360)
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        self.y += self.speed
        self.rect.y = self.y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_collision(self, rect):
        return self.rect.colliderect(rect)
