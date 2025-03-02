import pygame
import math
import random

# Initiera Pygame
pygame.init()

# Skärminställningar
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")

# Färger
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)  # Ej använd

# Spelvariabler
clock = pygame.time.Clock()
FPS = 60

# Klass för spelaren
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.angle = 0
        self.speed = 0
        self.radius = 20
        self.velocity_x = 0
        self.velocity_y = 0

    def draw(self):
        # Rita spelaren som en triangel
        tip_x = self.x + math.cos(math.radians(self.angle)) * self.radius
        tip_y = self.y - math.sin(math.radians(self.angle)) * self.radius
        left_x = self.x + math.cos(math.radians(self.angle + 120)) * self.radius
        left_y = self.y - math.sin(math.radians(self.angle + 120)) * self.radius
        right_x = self.x + math.cos(math.radians(self.angle - 120)) * self.radius
        right_y = self.y - math.sin(math.radians(self.angle - 120)) * self.radius
        pygame.draw.polygon(screen, BLUE, [(tip_x, tip_y), (left_x, left_y), (right_x, right_y)])

    def move(self):
        # Uppdatera position baserat på hastighet
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Wrap-around om spelaren går utanför skärmen
        if self.x > WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = WIDTH
        if self.y > HEIGHT:
            self.y = 0
        elif self.y < 0:
            self.y = HEIGHT

    def accelerate(self):
        # Öka hastigheten baserat på vinkeln
        self.velocity_x += math.cos(math.radians(self.angle)) * 0.1
        self.velocity_y -= math.sin(math.radians(self.angle)) * 0.1

    def decelerate(self):
        # Minska hastigheten
        self.velocity_x *= 0.99
        self.velocity_y *= 0.99

# Klass för asteroider
class Asteroid:
    def __init__(self, x=None, y=None, size=None, level=3): # Lägg till level
        self.x = x if x is not None else random.randint(0, WIDTH)
        self.y = y if y is not None else random.randint(0, HEIGHT)
        self.size = size if size is not None else random.randint(30, 50)
        self.level = level
        self.angle = random.randint(0, 360)
        self.speed = random.randint(1, 3)
        self.velocity_x = math.cos(math.radians(self.angle)) * self.speed
        self.velocity_y = -math.sin(math.radians(self.angle)) * self.speed

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.size, 2)

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Wrap-around om asteroiden går utanför skärmen
        if self.x > WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = WIDTH
        if self.y > HEIGHT:
            self.y = 0
        elif self.y < 0:
            self.y = HEIGHT

# Klass för skott
class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 10
        self.velocity_x = math.cos(math.radians(self.angle)) * self.speed
        self.velocity_y = -math.sin(math.radians(self.angle)) * self.speed
        self.radius = 3

    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

# Skapa spelaren, asteroider och skott
player = Player()
asteroids = [Asteroid() for _ in range(5)]
bullets = []

# Spelloop
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    # Hantera events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Tangentbordsinput
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.angle += 5
    if keys[pygame.K_RIGHT]:
        player.angle -= 5
    if keys[pygame.K_UP]:
        player.accelerate()
    if keys[pygame.K_DOWN]:
        player.decelerate()
    if keys[pygame.K_SPACE]:
        # Skapa ett nytt skott
        bullets.append(Bullet(player.x, player.y, player.angle))

    # Uppdatera och rita spelaren
    player.move()
    player.draw()

    # Uppdatera och rita asteroider
    for asteroid in asteroids:
        asteroid.move()
        asteroid.draw()

    # Uppdatera och rita skott
    for bullet in bullets:
        bullet.move()
        bullet.draw()

        # Ta bort skott som går utanför skärmen
        if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
            bullets.remove(bullet)

        # Kollisionsdetektion mellan skott och asteroider
        for asteroid in asteroids:
            distance = math.hypot(bullet.x - asteroid.x, bullet.y - asteroid.y)
            if distance < asteroid.size:
                #ta bort träffad asteroid
                asteroids.remove(asteroid)
                bullets.remove(bullet)

#dela upp asteroiden i två mindre om den inte är på lägsta nivå
                if asteroid.level > 1:
                    for _ in range(2):
                        new_asteroid = Asteroid(
                            x=asteroid.x,
                            y=asteroid.y,
                            size=asteroid.size // 2,
                            level=asteroid.level - 1
                        )
                        asteroids.append(new_asteroid)
                break
                
    pygame.display.flip()

pygame.quit()