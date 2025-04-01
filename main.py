import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

# Function to load the high score from a file
def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0  # Return 0 if the file does not exist

# Function to save the high score to a file
def save_high_score(high_score):
    with open("high_score.txt", "w") as file:
        file.write(str(high_score))

def main():
    pygame.init()
    print("Starting Asteroids!")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Load the high score at the start of the game
    high_score = load_high_score()

    text_font = pygame.font.SysFont("Arial", 25)

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)
    hit_count = 0
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    dt = 0

    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        if not game_over:
            updatable.update(dt)
            pygame.display.set_caption("Asteroids")
            screen.fill("black")
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    game_over = True
                    break
                for shot in shots:
                    if asteroid.collides_with(shot):
                        hit_count += 1
                        shot.kill()
                        asteroid.split()
        else:
            # Update the high score if needed
            if hit_count > high_score:
                high_score = hit_count
                save_high_score(high_score)  # Save the new high score to the file

            screen.fill("red")
            draw_text("GAME OVER", text_font, "black", SCREEN_WIDTH / 2 - 70, SCREEN_HEIGHT / 2 - 50)
            draw_text(f"High Score: {high_score}", text_font, "black", SCREEN_WIDTH / 2 - 80, SCREEN_HEIGHT / 2 + 30)

            # Add restart and quit logic here if needed

        draw_text(f"Score: {hit_count}", text_font, "white", 10, 20)
        for obj in drawable:
            obj.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
