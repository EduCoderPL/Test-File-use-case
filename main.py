import random
import pygame
from pygame.locals import *


class GameObject:
    def __init__(self, x, y, width, height, imgText):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velX = self.velY = 0
        self.rect = Rect(self.x, self.y, self.width, self.height)

        self.drawX = self.x
        self.drawY = self.y

        self.img = pygame.transform.scale(pygame.image.load(imgText), (self.width, self.height))

    def update_rect(self):
        self.rect = Rect(self.x, self.y, self.width, self.height)

    def solve_collision(self, listOfObjects):
        self.x += self.velX
        self.update_rect()

        for wall in listOfObjects:
            solve_rect_collisions(self, wall, "HORIZONTAL")

        self.y += self.velY
        self.update_rect()
        for wall in listOfObjects:
            solve_rect_collisions(self, wall, "VERTICAL")

    def draw(self):
        self.drawX = self.x - offsetX
        self.drawY = self.y - offsetY
        screen.blit(self.img, (self.drawX, self.drawY))


class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 48, "imgs/Panda Bojowa.png")
        self.moveLeft = self.moveRight = self.moveUp = self.moveDown = False
        self.path = []

    def update(self):
        self.input()
        self.update_rect()
        self.solve_collision(listOfWalls)

    def input(self):
        if self.moveLeft:
            self.velX -= 3
        if self.moveRight:
            self.velX += 3

        if self.moveUp:
            self.velY -= 3
        if self.moveDown:
            self.velY += 3

        self.moveLeft = self.moveRight = self.moveUp = self.moveDown = False


class Wall(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "imgs/Wall.png")


class Enemy(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, (0, 200, 0))

        self.path = []
        self.speed = 2

    def update(self):
        self.path.append((self.x, self.y))
        if len(self.path) > 10:
            self.path.pop(0)

        super().update_rect()
        self.solve_collision(listOfWalls)

    def follow(self, target):
        if self.x > target.x:
            self.velX = -self.speed
        if self.x < target.x:
            self.velX = self.speed

        if self.y > target.y:
            self.velY = -self.speed
        if self.y < target.y:
            self.velY = self.speed

    def draw(self):
        # for x, y in self.path:
        #     pygame.draw.rect(screen, (100, 100, 0), Rect(x, y, self.width, self.height))

        super().draw()

def solve_rect_collisions(object1, object2, dir):
    # Pilnuję, żeby prostokąt był zawsze na bieżaco w porównaniu do zmiennych x, y.
    object1.update_rect()

    if object1.rect.colliderect(object2.rect):

        if dir == "HORIZONTAL":
            # 4 funkcje sprawdzające kolizje z każdej strony.
            if object1.x + object1.width > object2.x > object1.x:
                object1.x = object2.x - object1.width

            elif object1.x < object2.x + object2.width < object1.x + object1.width:
                object1.x = object2.x + object2.width

        if dir == "VERTICAL":
            if object1.y + object1.height > object2.y > object1.y:
                object1.y = object2.y - object1.height

            elif object1.y < object2.y + object2.height < object1.y + object1.height:
                object1.y = object2.y + object2.height

        object1.update_rect()


SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

player = Player(100, 200)

listOfWalls = []
# for i in range(10):
#     rand_x = random.randint(0, 1000)
#     rand_y = random.randint(0, 800)

#     rand_width = random.randint(50, 400)
#     rand_height = random.randint(50, 400)
#     listOfWalls.append(Wall(rand_x, rand_y, rand_width, rand_height))

tile_size = 60
level = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

for y in range(len(level)):
    for x in range(len(level[0])):
        if level[y][x] == 1:
            new_x = x * tile_size
            new_y = y * tile_size
            listOfWalls.append(Wall(new_x, new_y, tile_size, tile_size))

offsetX = 0
offsetY = 0

#########################################################










running = True
while running:

    # Te trzy linijki pozwalają nam normalnie zamknąć program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    # UPDATE GRY:
    keys = pygame.key.get_pressed()

    player.velX = 0
    player.velY = 0

    if keys[K_d]:
        player.moveRight = True
    if keys[K_a]:
        player.moveLeft = True
    if keys[K_w]:
        player.moveUp = True
    if keys[K_s]:
        player.moveDown = True

    player.update()

    mousePos = pygame.mouse.get_pos()

    offsetX = player.x + mousePos[0] - SCREEN_WIDTH
    offsetY = player.y + mousePos[1] - SCREEN_HEIGHT

    screen.fill((0, 0, 0))

    for wall in listOfWalls:
        wall.draw()

    player.draw()

    # Czekanie na kolejną klatkę
    clock.tick(60)

    # Aktualizacja gry
    pygame.display.flip()
pygame.quit()
