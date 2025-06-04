import pygame


class Spaceship:
    def __init__(self, width, height, speed):
        self.x = 300 // 2 - width // 2
        self.y = 600 - height - 10
        self.width = width
        self.height = height
        self.speed = speed
        self.max_shots = 5
        self.health = 100
        self.image = pygame.image.load('./assets/img/spaceship_image.png')
        self.image = pygame.transform.scale(self.image,
                                            (self.width, self.height)
                                            )
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < 600 - self.height:
            self.y += self.speed
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < 300 - self.width:
            self.x += self.speed

        self.rect.x = self.x
        self.rect.y = self.y


class Laser:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 20
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        self.y -= self.speed
        self.rect.y = self.y

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
