import pygame
import math as m


def x_trajectory(x_basis, x_speed, t):
    x = x_basis + (x_speed * t)
    return x


def y_trajectory(y_basis, y_speed, t):
    y = y_basis - (-9.81 * t ** 2 / 2 + y_speed * t)
    return y


def x_linear(x, x_speed):
    x += (x_speed * 0.1)
    return x


def y_linear(y, y_speed):
    y += (y_speed * 0.1) + 9.81 * t ** 2 / 2
    return y


# Define some colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Initial Position of the square
x = x_basis = 0
y = y_basis = 80
speed = 50
angle = 0.78539816339
x_speed = m.cos(angle)*speed
y_speed = m.sin(angle)*speed
t = 0

pygame.init()

# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Physics test")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Game logic should go here

    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blitting the
    # background image.
    screen.fill(BLACK)

    # --- Drawing code should go here
    rect_test = ((x, y), (10, 10))
    platform = ((400, 400), (100, 10))
    platform_2 = ((600, 400), (10,50))
    pygame.draw.rect(screen, RED, rect_test)
    pygame.draw.rect(screen, BLUE, platform)
    pygame.draw.rect(screen, GREEN, platform_2)
    if 500 > x > 400 and 393 > y > 385:
        y = 390
        y_speed = 0
        x = x_linear(x, x_speed)
        x_basis = x
        y_basis = y
        t = 0
    if 588 < x < 593 and 400 < y < 450:
        x = 590
        x_speed = 0
        y = y_trajectory(y_basis, y_speed, t)
        x_basis = x
        t += 0.1
    else:
        x = x_trajectory(x_basis, x_speed, t)
        y = y_trajectory(y_basis, y_speed, t)
        t += 0.1
    if y > 500 or x > 700:
        x = x_basis = 0
        y = y_basis = 80
        speed = 50
        angle = 0.78539816339
        x_speed = m.cos(angle) * speed
        y_speed = m.sin(angle) * speed
        t = 0
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
