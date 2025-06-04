import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Game settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60
ASTEROID_SPEED = 5
ASTEROID_SPAWN_RATE = 25  # Lower value = more frequent asteroid spawn
SHIP_SPEED = 5
MAX_ASTEROIDS = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spaceship Evader")

# Load spaceship image
ship_width = 50
ship_height = 60
ship = pygame.Surface((ship_width, ship_height))
ship.fill(WHITE)

# Asteroid settings
asteroid_width = 40
asteroid_height = 40
asteroids = []

# Game variables
player_health = 100
player_x = SCREEN_WIDTH // 2 - ship_width // 2
player_y = SCREEN_HEIGHT - ship_height - 10
player_velocity = 0
running = True
start_time = time.time()

# Font for displaying text
font = pygame.font.SysFont("Arial", 20)


# Function to draw the player's spaceship
def draw_ship(x, y):
    screen.blit(ship, (x, y))


# Function to generate a new asteroid
def generate_asteroid():
    x_pos = random.randint(0, SCREEN_WIDTH - asteroid_width)
    y_pos = -asteroid_height
    speed = random.randint(3, 7)
    asteroid = pygame.Rect(x_pos, y_pos, asteroid_width, asteroid_height)
    asteroids.append((asteroid, speed))


# Function to display the health on the screen
def display_health(health):
    health_text = font.render(f"Health: {health}", True, WHITE)
    screen.blit(health_text, (10, 10))


# Function to detect collisions between the ship and asteroids
def check_collision(ship_rect, asteroids):
    for asteroid, _ in asteroids:
        if ship_rect.colliderect(asteroid):
            return True
    return False


# Main game loop
while running:
    screen.fill(BLACK)
    elapsed_time = time.time() - start_time

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key press handling for movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= SHIP_SPEED
    if keys[pygame.K_DOWN] and player_y < SCREEN_HEIGHT - ship_height:
        player_y += SHIP_SPEED
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= SHIP_SPEED
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - ship_width:
        player_x += SHIP_SPEED

    # Update asteroid positions and spawn new asteroids
    for asteroid, speed in asteroids:
        asteroid.y += speed

    # Remove off-screen asteroids
    asteroids = [(asteroid, speed) for asteroid,
                 speed in asteroids if asteroid.y < SCREEN_HEIGHT
                 ]

    # Randomly spawn new asteroids
    if random.randint(1,
                      ASTEROID_SPAWN_RATE
                      ) == 1 and len(asteroids) < MAX_ASTEROIDS:
        generate_asteroid()

    # Check for collisions
    ship_rect = pygame.Rect(player_x, player_y, ship_width, ship_height)
    if check_collision(ship_rect, asteroids):
        player_health -= 50
        asteroids = []  # Clear asteroids on collision to reset the state
        if player_health <= 0:
            running = False  # Game over if health reaches 0

    # Draw health
    display_health(player_health)

    # Draw the spaceship
    draw_ship(player_x, player_y)

    # Draw asteroids
    for asteroid, _ in asteroids:
        pygame.draw.rect(screen, RED, asteroid)

    # End game condition: after a certain time
    if elapsed_time > 30:  # Game ends after 30 seconds
        running = False

    # Update the screen
    pygame.display.flip()
    pygame.time.Clock().tick(FPS)

# End of the game
pygame.quit()
