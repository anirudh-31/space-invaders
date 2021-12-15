import pygame
import random
from math import *
from pygame import mixer

pygame.init()  # initializing pygame

# creating screen and setting its
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("background.png")

# window title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player configurations
playerImg = pygame.image.load("space-invaders.png")
playerX = 370
playerY = 480
playerX_change = 0

# enemy configurations
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

for enemy in range(num_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(random.randint(1, 5))
    enemyY_change.append(random.randint(10, 50))

# bullet configuration
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 40
bullet_state = "ready"
bullet_sound = mixer.Sound("shot.wav")

# Score
score_value = 1
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# game over text
game_font = pygame.font.Font("freesansbold.ttf", 64)


# displays the score
def display_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# displays the player
def player(x, y):
    screen.blit(playerImg, (x, y))


# displays the enemy
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# displays the bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# checks if the bullet hits the enemy
def check_collision(enemyx, enemyy, bulletx, bullety):
    x = pow((enemyx - bulletx), 2)
    y = pow((enemyy - bullety), 2)
    dist = sqrt(x + y)
    if dist < 27:
        return True
    return False


# displays text when the game is over
def game_over(score):
    game_over_text = game_font.render("Game Over", True, (255, 255, 255))
    score_text = font.render("Your Score : " + str(score), True, (255, 255, 255))
    screen.blit(game_over_text, (200, 250))
    screen.blit(score_text, (200, 350))

# Game loop
run = True
while run:  # infinite loop which stops running only whe the close button is clicked

    screen.fill((0, 0, 0))  # setting a color background
    screen.blit(background, (0, 0))  # setting the background image

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # player movement and shooting controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                playerX_change = -5

            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_change = 5

            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

    # boundary controls for player
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # enemy movement control
    for i in range(num_enemies):

        # ending the game
        if enemyY[i] > 440 :
            for j in range(num_enemies):
                enemyY[j] = 2000
            game_over(score_value)
            break

        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
        enemyX[i] += enemyX_change[i]  # heck if necessary

        collision = check_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            mixer.Sound("explosion.wav").play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement control
    if bulletY <= 0:
        bullet_state = 'ready'
        bulletY = 480
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    display_score(textX, textY)
    pygame.display.update()  # updating the screen
