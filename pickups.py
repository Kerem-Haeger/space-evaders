import pygame
import random


class Pickup:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20  # Size of the pickup (adjustable)
        self.type = random.choice([
            "speed_up",
            "speed_down",
            "extra_shots",
            "health"
            ])
        self.image = self.load_image(self.type)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def load_image(self, pickup_type):
        """Load different images based on the pickup type."""
        surface = pygame.Surface((self.size, self.size))
        if pickup_type == "speed_up":
            surface.fill((0, 255, 0))  # Green for speed up
        elif pickup_type == "speed_down":
            surface.fill((255, 0, 0))  # Red for speed down
        elif pickup_type == "extra_shots":
            surface.fill((0, 0, 255))  # Blue for extra shots
        elif pickup_type == "health":
            surface.fill((255, 0, 255))  # Purple for health
        return surface

    def move(self, speed):
        """Move the pickup downward to simulate falling."""
        self.y += speed
        self.rect.y = self.y

    def draw(self, screen):
        """Draw the pickup on the screen."""
        screen.blit(self.image, self.rect.topleft)

    def check_collision(self, rect):
        """Check if the pickup collides with the player's spaceship."""
        return self.rect.colliderect(rect)

    def apply_effect(self, player):
        """Apply the effect of the pickup to the player."""
        if self.type == "speed_up":
            player.speed += 3
        elif self.type == "speed_down":
            player.speed -= 1
        elif self.type == "extra_shots":
            player.max_shots += 1
        elif self.type == "health":
            player.health += 50
            if player.health > 100:  # Ensure health doesn't exceed the maximum
                player.health = 100
