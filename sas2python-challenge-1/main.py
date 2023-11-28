import pygame
import random

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Flappy Bird")

# Load images
bird_img = pygame.Surface((30, 30))  # Placeholder for bird image
bird_img.fill((255, 255, 0))  # Filling the bird image with yellow color
background_img = pygame.Surface(screen.get_size())
background_img.fill((135, 206, 235))  # Light blue background
pipe_img = pygame.Surface((50, 200))  # Placeholder for pipe image
pipe_img.fill((0, 128, 0))  # Filling the pipe image with green color

# Game variables
bird_y = 300
bird_speed = 0
gravity = 0.5
pipe_x = 400
gap = 200
pipe_speed = 2
score = 0

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_speed = -10

    # Update game state
    bird_speed += gravity
    bird_y += bird_speed
    pipe_x -= pipe_speed

    # Collision detection
    if bird_y > 570 or bird_y < 0:
        running = False  # End the game if the bird hits the ground or flies too high

    # Reset pipe
    if pipe_x < -50:
        pipe_x = 400
        score += 1

    # Draw everything
    screen.blit(background_img, (0, 0))
    screen.blit(bird_img, (50, bird_y))
    screen.blit(pipe_img, (pipe_x, 0))
    screen.blit(pipe_img, (pipe_x, 400 + gap))

    # Update display
    pygame.display.update()

    # Cap the frame rate
    pygame.time.Clock().tick(30)

# Quit Pygame
pygame.quit()