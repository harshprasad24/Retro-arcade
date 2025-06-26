import pygame
import random
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
GRAY = (128, 128, 128)

# Initialize display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Dodging Asteroids")
clock = pygame.time.Clock()

class Spaceship:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 60
        self.width = 40
        self.height = 30
        self.speed = 5
    
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - self.height:
            self.y += self.speed
    
    def draw(self, screen):
        pygame.draw.polygon(screen, BLUE, [
            (self.x + self.width//2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ])
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Asteroid:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 30)
        self.y = -30
        self.size = random.randint(20, 40)
        self.speed = random.randint(2, 5)
    
    def move(self):
        self.y += self.speed
    
    def draw(self, screen):
        pygame.draw.circle(screen, GRAY, (self.x + self.size//2, self.y + self.size//2), self.size//2)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)
    
    def is_off_screen(self):
        return self.y > HEIGHT

def main():
    spaceship = Spaceship()
    asteroids = []
    score = 0
    font = pygame.font.Font(None, 36)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        spaceship.move(keys)
        
        # Spawn asteroids
        if random.randint(1, 30) == 1:
            asteroids.append(Asteroid())
        
        # Move asteroids
        for asteroid in asteroids[:]:
            asteroid.move()
            if asteroid.is_off_screen():
                asteroids.remove(asteroid)
                score += 1
        
        # Check collisions
        spaceship_rect = spaceship.get_rect()
        for asteroid in asteroids:
            if spaceship_rect.colliderect(asteroid.get_rect()):
                print(f"Game Over! Final Score: {score}")
                running = False
        
        # Draw everything
        screen.fill(BLACK)
        spaceship.draw(screen)
        for asteroid in asteroids:
            asteroid.draw(screen)
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()