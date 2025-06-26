import pygame
import random
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Shooter Game")
clock = pygame.time.Clock()

class Player:
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
    
    def draw(self, screen):
        pygame.draw.polygon(screen, BLUE, [
            (self.x + self.width//2, self.y),
            (self.x, self.y + self.height),
            (self.x + self.width, self.y + self.height)
        ])
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 4
        self.height = 10
        self.speed = 7
    
    def move(self):
        self.y -= self.speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.width, self.height))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def is_off_screen(self):
        return self.y < 0

class Enemy:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 30)
        self.y = -30
        self.width = 30
        self.height = 30
        self.speed = random.randint(1, 3)
    
    def move(self):
        self.y += self.speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def is_off_screen(self):
        return self.y > HEIGHT

def main():
    player = Player()
    bullets = []
    enemies = []
    score = 0
    font = pygame.font.Font(None, 36)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player.x + player.width//2 - 2, player.y))
        
        keys = pygame.key.get_pressed()
        player.move(keys)
        
        # Move bullets
        for bullet in bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                bullets.remove(bullet)
        
        # Spawn enemies
        if random.randint(1, 60) == 1:
            enemies.append(Enemy())
        
        # Move enemies
        for enemy in enemies[:]:
            enemy.move()
            if enemy.is_off_screen():
                enemies.remove(enemy)
        
        # Check bullet-enemy collisions
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.get_rect().colliderect(enemy.get_rect()):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10
                    break
        
        # Check player-enemy collisions
        player_rect = player.get_rect()
        for enemy in enemies:
            if player_rect.colliderect(enemy.get_rect()):
                print(f"Game Over! Final Score: {score}")
                running = False
        
        # Draw everything
        screen.fill(BLACK)
        player.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()