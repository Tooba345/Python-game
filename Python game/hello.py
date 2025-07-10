import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Star")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 128, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.SysFont("Comic Sans MS", 64)
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 48)

# Load images
galaxy_background = pygame.image.load("background image 1.jpg")
galaxy_background = pygame.transform.scale(galaxy_background, (WIDTH, HEIGHT))

star_image = pygame.image.load("star.png")
star_image = pygame.transform.scale(star_image, (40, 40))  # Scale the star image

ufo_image = pygame.image.load("ufo.png")
ufo_image = pygame.transform.scale(ufo_image, (55, 55))  # Scale the UFO image

basket_image = pygame.image.load("basket.png")
basket_image = pygame.transform.scale(basket_image, (70, 70))  # Scale the basket image

# Player properties
basket_width = 70
basket_height = 50
player_x = WIDTH // 2
player_y = HEIGHT - 70
player_speed = 7

# Star properties (collectibles)
star_size = 30

# Obstacle properties
ufo_size = 50
obstacle_speed_increment = 2

# Levels
level = 1
stars = [{'x': random.randint(0, WIDTH - star_size), 'y': random.randint(-600, 0), 'speed': 5}]
ufos = [{'x': random.randint(0, WIDTH - ufo_size), 'y': random.randint(-600, 0), 'speed': 5}]
level_up_score = 5  # Score needed to level up

# Score
score = 0


# Functions
def display_text(text, font, color, x, y):
    screen.blit(font.render(text, True, color), (x, y))


def display_score_and_level(score, level):
    display_text(f"Score: {score}", font, WHITE, 10, 10)
    display_text(f"Level: {level}", font, WHITE, WIDTH - 120, 10)


def start_screen():
    while True:
        # Draw the background image\
        screen.blit(galaxy_background, (0, 0))

        pygame.image.load("galaxy_background.jpg"),(0, 0)

        # Title text
        display_text("Shooting Star", title_font, BLUE, WIDTH // 2 - 220, HEIGHT // 2 - 200)

        # Credit text
        display_text("Game made by Tooba", font, WHITE, WIDTH // 2 - 90, HEIGHT // 2 - 120)

        # Buttons
        play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 50)

        pygame.draw.rect(screen, WHITE, play_button)
        pygame.draw.rect(screen, WHITE, quit_button)

        display_text("Play", font, BLACK, WIDTH // 2 - 30, HEIGHT // 2 + 10)
        display_text("Quit", font, BLACK, WIDTH // 2 - 30, HEIGHT // 2 + 90)

        pygame.display.flip()

        # Event handling for buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


# Main game loop
def main():
    global player_x, stars, ufos, level, score

    running = True
    while running:
        # Draw galaxy background image
        screen.blit(galaxy_background, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - basket_width:
            player_x += player_speed

        # Update stars
        for star in stars:
            star['y'] += star['speed']
            if star['y'] > HEIGHT:
                star['y'] = random.randint(-100, 0)
                star['x'] = random.randint(0, WIDTH - star_size)

            # Check collision with player (basket)
            if (player_x < star['x'] < player_x + basket_width or
                player_x < star['x'] + star_size < player_x + basket_width) and \
               (player_y < star['y'] + star_size < player_y + basket_height):
                score += 1
                star['y'] = random.randint(-100, 0)
                star['x'] = random.randint(0, WIDTH - star_size)

        # Update UFOs (obstacles)
        for ufo in ufos:
            ufo['y'] += ufo['speed']
            if ufo['y'] > HEIGHT:
                ufo['y'] = random.randint(-100, 0)
                ufo['x'] = random.randint(0, WIDTH - ufo_size)

            # Check collision with player
            if (player_x < ufo['x'] < player_x + basket_width or
                player_x < ufo['x'] + ufo_size < player_x + basket_width) and \
               (player_y < ufo['y'] + ufo_size < player_y + basket_height):
                # Game Over
                display_text("GAME OVER!", big_font, RED, WIDTH // 2 - 150, HEIGHT // 2 - 50)
                pygame.display.flip()
                pygame.time.wait(2000)
                running = False
                return

        # Level up
        if score >= level_up_score * level:
            level += 1
            # Increase the number of stars and UFOs
            stars.append({'x': random.randint(0, WIDTH - star_size), 'y': random.randint(-600, 0), 'speed': 5 + level})
            ufos.append({'x': random.randint(0, WIDTH - ufo_size), 'y': random.randint(-600, 0), 'speed': 5 + level + obstacle_speed_increment})

        # Draw basket (player)
        screen.blit(basket_image, (player_x, player_y))

        # Draw stars (collectibles)
        for star in stars:
            screen.blit(star_image, (star['x'], star['y']))

        # Draw UFOs (obstacles)
        for ufo in ufos:
            screen.blit(ufo_image, (ufo['x'], ufo['y']))

        # Display score and level
        display_score_and_level(score, level)

        # Update the display
        pygame.display.flip()

        # Control frame rate
        clock.tick(30)


# Start the game
if __name__ == "__main__":
    start_screen()
    main()

