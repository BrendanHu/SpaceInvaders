import random  # for enemy position
import math  # for distance calculations
import pygame
from pygame import mixer
# Initialize pygame
pygame.init()
# Creates a 800x600 (width by height) screen
screen = pygame.display.set_mode((800, 600))  # Note: using a while True loop can keep the screen on longer (instead of only during execution), but has problems itself
# Title and Icon
pygame.display.set_caption("Space Invaders")  # title
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
# Background image
background = pygame.image.load("space.jpg")
# Background sandstorm
mixer.music.load('sandstorm.wav')
mixer.music.play(-1)  # -1 makes it loop
# Player
playerImage = pygame.image.load("spaceship.png")
playerX = 370
playerY = 480
delta_player_x = 0
# Enemies
enemyImage = []
enemyX = []
enemyY = []
delta_enemy_x = []
delta_enemy_y = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImage.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    delta_enemy_x.append(4)
    delta_enemy_y.append(30)
# Bullet
bulletImage = pygame.image.load("bullet.png")
bulletX = 0  # will be changed within while loop
bulletY = 480
delta_bullet_x = 0
delta_bullet_y = 5
bullet_state = "ready"  # ready: bullet is not visible on screen | fired: bullet is visible on the screen
lost = False
# Score
score_value = 0
font = pygame.font.Font('Sting.otf', 32)

textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('Sting.otf', 72)

textX = 10
textY = 10


def show_score(x, y):
    """Displays score in top left of screen."""
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    """Displays text when the game is over."""
    over_text = over_font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def restart_text():
    """Displays restart instructions when the game is over."""
    restart_text = font.render("Press R to restart", True, (255, 255, 255))
    screen.blit(restart_text, (250, 375))


def player(x, y):  # parameters x and y can be sent in continously as a response to keypresses
    """Draws the player model on the screen."""
    screen.blit(playerImage, (x, y))  # blit() = draw()


def enemy(x, y, i):
    """Draws enemy models on the screen."""
    screen.blit(enemyImage[i], (x, y))


def fire_bullet(x, y):
    """Draws bullet when fired."""
    global bullet_state
    bullet_state = "fired"
    screen.blit(bulletImage, (x + 16, y + 10))  # ensures bullet appears at the right spot on the ship (trial and error)


def isCollision(enemyX, enemyY, bulletX, bulletY):
    """Determines whether or not a fired bullet has hit the enemy."""
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# --------------------------- GAME LOOP --------------------------------------
running = True
while running:
    # Anything that must be persistent (background, characters) must be inside the while loop
    # Below is how to fill background with single color w/ RGB tuple
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))  # draw background on screen from origin
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # checks for quit button keypress
            running = False
    # If key pressed, check if it's right or left
    if event.type == pygame.KEYDOWN:  # KEYDOWN is ANY key on the keyboard, not the down arrow (i.e key --> down)
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            delta_player_x = -5  # move left
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            delta_player_x = 5  # move right
        if event.key == pygame.K_SPACE and bullet_state == "ready" and lost is False:  # fire bullet
            bullet_sound = mixer.Sound('laser.wav')
            bullet_sound.play()
            bulletX = playerX  # get current x coordinate of the ship (but do not update)
            fire_bullet(bulletX, bulletY)
        # Restart game
        if event.key == pygame.K_r and lost is True:
            playerY = 480
            playerX = 370
            # Enemies
            enemyImage = []
            enemyX = []
            enemyY = []
            delta_enemy_x = []
            delta_enemy_y = []
            num_of_enemies = 6

            for i in range(num_of_enemies):
                enemyImage.append(pygame.image.load("enemy.png"))
                enemyX.append(random.randint(65, 735))
                enemyY.append(random.randint(50, 150))
                delta_enemy_x.append(3)
                delta_enemy_y.append(25)

            score_value = 0
            lost = False

    if event.type == pygame.KEYUP:  # When key is released (key --> up)
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
            delta_player_x = 0  # released key --> stop player
    # Player movement
    playerX += delta_player_x  # updates position of the player
    # Add boundaries so the ship doesn't fly off the map
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # Taking into account that the ship is 64 pixels wide
        playerX = 736
    # Enemy movement
    for i in range(num_of_enemies):
        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            playerY = 2000
            game_over_text()
            restart_text()
            lost = True
            break
        enemyX[i] += delta_enemy_x[i]
        if enemyX[i] <= 0:
            delta_enemy_x[i] = -delta_enemy_x[i]
            enemyY[i] += delta_enemy_y[i]
        if enemyX[i] >= 735:
            delta_enemy_x[i] = -delta_enemy_x[i]
            enemyY[i] += delta_enemy_y[i]
        # Collision detection
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:  # reset game conditions
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # Bullet movement
    if bulletY <= 0:  # Reloads the bullet if it passes the top of the screen
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fired":
        fire_bullet(bulletX, bulletY)
        bulletY -= delta_bullet_y  # The first instance of moving the bullet (once it's state is fired, obviously.)

    player(playerX, playerY)  # Note: must render the player after the background (or it would be drawn over)
    show_score(textX, textY)
    pygame.display.update()  # Makes the display (game window) update every loop of code
