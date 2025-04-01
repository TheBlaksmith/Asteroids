import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    print("Starting Asteroids!")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
   
    text_font = pygame.font.SysFont("Arial", 25)

    def game_over(time):
        player.kill()
        print(f"Your score: {hit_count}")
        print(f"High Score to beat: 5,000")
        print("GAME OVER!")
        screen.fill("white")
        for i in range(1, time):
            draw_text("GAME OVER",text_font, "black", SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
            if i == time:
                sys.exit()


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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        updatable.update(dt)
        pygame.display.set_caption("Asteroids")
        screen.fill("black")
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                asteroid.kill()
                game_over(5)
            for shot in shots:
                if asteroid.collides_with(shot):
                    hit_count += 1
                    shot.kill()
                    asteroid.split()
    
        
        draw_text(f"Score: {hit_count}", text_font, "white", 10, 20)
        for obj in drawable:
            obj.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()