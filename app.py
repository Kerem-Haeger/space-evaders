import pygame
import random
from pickups import Pickup
from player import Spaceship, Laser
from asteroid import Asteroid
from game_settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SHIP_WIDTH,
    SHIP_HEIGHT,
    SHIP_SPEED,
    PURPLE,
    WHITE
)

# Initialize Pygame
pygame.init()

# Setup the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Evader")

# Create the spaceship object
ship = Spaceship(SHIP_WIDTH, SHIP_HEIGHT, SHIP_SPEED)

# Create a list for asteroids and lasers
asteroids = []
lasers = []
pickups = []
laser_fired = False
score = 0

# Star background setup
star_positions = []
for _ in range(100):
    star_x = random.randint(0, SCREEN_WIDTH)
    star_y = random.randint(0, SCREEN_HEIGHT)
    star_size = random.randint(0, 2)
    star_positions.append((star_x, star_y, star_size))

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle key press (SPACEBAR) to fire laser
        if event.type == pygame.KEYDOWN:
            if (
                event.key == pygame.K_SPACE
                and ship.max_shots > 0
                and not laser_fired
            ):
                laser = Laser(ship.x + SHIP_WIDTH // 2 - 2, ship.y)
                lasers.append(laser)  # Add laser to the list
                ship.max_shots -= 1  # Decrease shots available
                laser_fired = True

            # Handle ESC key to quit the game
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            laser_fired = False

    # Fill the screen with the background color
    screen.fill(PURPLE)

    # Draw the static stars
    for (star_x, star_y, star_size) in star_positions:
        pygame.draw.circle(screen, WHITE, (star_x, star_y), star_size)

    # Move the spaceship
    ship.move()

    # Spawn new asteroids at random intervals
    if random.randint(1, 40) == 1:
        new_asteroid = Asteroid(random.randint(0, SCREEN_WIDTH - 40),
                                -40,
                                random.randint(2, 4)
                                )
        asteroids.append(new_asteroid)

    # Spawn new pickups at random intervals
    if random.randint(1, 200) == 1:
        new_pickup = Pickup(random.randint(0, SCREEN_WIDTH - 20), -20)
        pickups.append(new_pickup)

    # Move and draw the asteroids
    for asteroid in asteroids[:]:
        asteroid.move()
        asteroid.draw(screen)

        # Check if asteroid goes off the bottom of the screen
        if asteroid.y > SCREEN_HEIGHT:
            asteroids.remove(asteroid)  # Remove the asteroid
            score += 10  # Increase score by 10

        if asteroid.check_collision(ship.rect):
            ship.health -= 50  # Deduct health on collision
            asteroids.remove(asteroid)  # Remove the asteroid after collision
            if ship.health <= 0:
                running = False  # End the game if health reaches 0

        # Check for laser-asteroid collision
        for laser in lasers[:]:
            if asteroid.check_collision(laser.rect):
                asteroids.remove(asteroid)  # Remove asteroid on collision
                lasers.remove(laser)  # Remove laser on collision
                break

    # Move and draw the lasers
    for laser in lasers[:]:
        laser.move()
        laser.draw(screen)

        if laser.y < 0:
            lasers.remove(laser)

    # Move and draw the pickups
    for pickup in pickups[:]:
        pickup.move(2)  # Speed of falling pickups
        pickup.draw(screen)

        if pickup.check_collision(ship.rect):  # If pickup is collected
            pickup.apply_effect(ship)  # Apply its effect to the player
            pickups.remove(pickup)  # Remove the pickup after it's collected

    # Draw the spaceship
    screen.blit(ship.image, (ship.x, ship.y))

    # Display the health and shots remaining
    font = pygame.font.SysFont("Arial", 15)
    health_text = font.render(f"Health: {ship.health}", True, WHITE)
    screen.blit(health_text, (10, 10))

    shots_text = font.render(f"Shots: {ship.max_shots}", True, WHITE)
    screen.blit(shots_text, (SCREEN_WIDTH - 100, 10))

    # Display the score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - 40, 10))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
