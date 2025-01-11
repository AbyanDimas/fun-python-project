import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PIPE_WIDTH = 50
PIPE_GAP = 150
GRAVITY = 0.5
FLAP_STRENGTH = -10

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

clock = pygame.time.Clock()

# Bird class
class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.radius = 15

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        pygame.draw.circle(screen, BLACK, (self.x, int(self.y)), self.radius)

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.top = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
        self.bottom = self.top + PIPE_GAP

    def move(self):
        self.x -= 5

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, 0, PIPE_WIDTH, self.top))
        pygame.draw.rect(screen, BLACK, (self.x, self.bottom, PIPE_WIDTH, SCREEN_HEIGHT - self.bottom))

    def is_off_screen(self):
        return self.x + PIPE_WIDTH < 0

# Main game function
def flappy_bird():
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH)]
    score = 0

    running = True
    while running:
        screen.fill(WHITE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.flap()

        # Bird movement
        bird.move()
        bird.draw()

        # Pipe movement
        for pipe in pipes:
            pipe.move()
            pipe.draw()

            # Check collision
            if bird.y - bird.radius < pipe.top or bird.y + bird.radius > pipe.bottom:
                if pipe.x < bird.x < pipe.x + PIPE_WIDTH:
                    running = False

        # Add new pipes
        if pipes[-1].x < SCREEN_WIDTH // 2:
            pipes.append(Pipe(SCREEN_WIDTH))
        if pipes[0].is_off_screen():
            pipes.pop(0)
            score += 1

        # Check ground collision
        if bird.y + bird.radius > SCREEN_HEIGHT:
            running = False

        # Display score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(text, (10, 10))

        # Update screen
        pygame.display.flip()
        clock.tick(30)

    print(f"Game Over! Your Score: {score}")
    pygame.quit()
    sys.exit()

# Run the game
flappy_bird()
