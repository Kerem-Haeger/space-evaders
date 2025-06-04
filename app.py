import pygame
import random
# import time

# Initialize Pygame
pygame.init()

# Game settings
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Evader")

DARK_BLUE = (0, 0, 50)  # A deep dark blue for the space background
PURPLE = (25, 25, 50)  # A darker purple for variation
WHITE = (255, 255, 255)  # White for stars

star_positions = []

for _ in range(100):  # Create 100 stars
    star_x = random.randint(0, SCREEN_WIDTH)
    star_y = random.randint(0, SCREEN_HEIGHT)
    star_size = random.randint(0, 2)  # Random size for stars
    star_positions.append((star_x, star_y, star_size))

# Game settings
SHIP_WIDTH = 50
SHIP_HEIGHT = 60
SHIP_SPEED = 4  # How fast the spaceship moves (in pixels per frame)

ship = pygame.image.load('./assets/img/spaceship_image.png')
ship = pygame.transform.scale(ship, (SHIP_WIDTH, SHIP_HEIGHT))
ship = ship.convert_alpha()

# Initial position (starting at the center of the screen)
player_x = SCREEN_WIDTH // 2 - SHIP_WIDTH // 2  # Center horizontally
player_y = SCREEN_HEIGHT - SHIP_HEIGHT - 10

asteroid_image = pygame.image.load('./assets/img/asteroid.png')


class Asteroid:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed  # Speed at which the asteroid falls

        # Random size for the asteroid (between 20 and 50 pixels)
        self.size = random.randint(20, 50)

        # Scale the asteroid image to a random size
        self.image = pygame.transform.scale(asteroid_image,
                                            (self.size, self.size)
                                            )

        # Random rotation (between 0 and 360 degrees)
        self.rotation = random.randint(0, 360)
        self.image = pygame.transform.rotate(self.image, self.rotation)

        # Get the new rect for the rotated image to update its position
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        """Move the asteroid down the screen"""
        self.y += self.speed
        self.rect.y = self.y  # Update the rect’s y position

    def draw(self, screen):
        """Draw the asteroid on the screen (as a rotated image)"""
        screen.blit(self.image, self.rect)

    def check_collision(self, player_rect):
        """Check if the asteroid collides with the player's spaceship"""
        if self.rect.colliderect(player_rect):
            return True  # Collision detected
        return False


def move_player(player_x, player_y, SHIP_SPEED):
    keys = pygame.key.get_pressed()

    # Handle movement
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= SHIP_SPEED  # Move up
    if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - SHIP_HEIGHT:
        player_y += SHIP_SPEED  # Move down
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= SHIP_SPEED  # Move left
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - SHIP_WIDTH:
        player_x += SHIP_SPEED  # Move right

    # Handle ESC key to quit
    if keys[pygame.K_ESCAPE]:
        return player_x, player_y, False

    return player_x, player_y, True


# Game loop
running = True
asteroids = []
player_health = 100

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with the base background color
    screen.fill(PURPLE)

    # Draw the static stars (only once generated)
    for (star_x, star_y, star_size) in star_positions:
        pygame.draw.circle(screen, WHITE, (star_x, star_y), star_size)

    # Call the move_player function to update the player position
    player_x, player_y, running = move_player(player_x, player_y, SHIP_SPEED)

    # Create a rect for the player's spaceship (for collision detection)
    player_rect = pygame.Rect(player_x, player_y, SHIP_WIDTH, SHIP_HEIGHT)

    # Spawn new asteroids at random intervals
    if random.randint(1, 30) == 1:
        new_asteroid = Asteroid(random.randint(0, SCREEN_WIDTH - 40),
                                -40,
                                random.randint(2, 4)
                                )
        asteroids.append(new_asteroid)

    # Move and draw the asteroids
    for asteroid in asteroids:
        asteroid.move()
        asteroid.draw(screen)

        # Check if asteroid collides with the spaceship
        if asteroid.check_collision(player_rect):
            player_health -= 50  # Deduct health on collision
            asteroids.remove(asteroid)  # Remove the asteroid after collision
            if player_health <= 0:
                running = False  # End the game if health reaches 0

    screen.blit(ship, (player_x, player_y))

    # Display the health
    font = pygame.font.SysFont("Arial", 20)
    health_text = font.render(f"Health: {player_health}", True, WHITE)
    screen.blit(health_text, (10, 10))

    # Update the screen
    pygame.display.flip()

    # Frame rate control
    pygame.time.Clock().tick(60)

# Quit Pygame after the loop ends
pygame.quit()
