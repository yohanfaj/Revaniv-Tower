# REVNANIV'S TOWER - main.py
# A game developed by Adrien BARBIER, Yohan FAJERMAN, Danny GRAINE, Elouan LARROCHE & Camille SALAUN
# EFREI PARIS - L1 Int 1 (Team 81) Promo 2025 – Transversal Project L1

# This file contains the entire code of our game.
# You will find firstly the initialization of some constants & variables and of the assets,
# then some functions and finally the main loop of the game


import pygame, sys, time
from pygame.locals import *
from random import randint

pygame.mixer.pre_init(44100, -16, 2, 512)

# ------------------------------------------------------------------------------------


# CONSTANTS & VARIABLES:

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

FPS = 60
PLAYERMOVERATE_X = 4  # Movements of the player in "pixels/loop".
PLAYERMOVERATE_Y = 10
tomato1moverate = tomato2moverate = tomato3moverate = 0
timer = t_beer = beer_cooldown = 0
beer_x = 0

HEALTH = 3  # Initial Health of the player
BONUS = 5000  # Initial score of the player
bonus_cpt = 0

# Some boolean variables, useful to control the behaviour of some objects:
isJump = False
tomato1jump = tomato2jump = tomato3jump = False
beer_launched = False
potion_checked = True

finalscore = 0
death = [0, 0]  # List which will count the 2 ways of loosing: by projectiles or by time.


# PLATFORMS INITIALIZATION:
P1_X = 0
P1_Y = 590
P1_LX = 600
P_Y = 10
P1 = pygame.Rect(P1_X, P1_Y, P1_LX, P_Y)
isOnP1 = False
P2_X = 0
P2_Y = 470
P2_LX = 450
P2 = pygame.Rect(P2_X, P2_Y, P2_LX, P_Y)
isOnP2 = False
P3_X = 150
P3_Y = 350
P3_LX = 450
P3 = pygame.Rect(P3_X, P3_Y, P3_LX, P_Y)
isOnP3 = False
P4_X = 0
P4_Y = 230
P4_LX = 450
P4 = pygame.Rect(P4_X, P4_Y, P4_LX, P_Y)
isOnP4 = False

# ------------------------------------------------------------------------------------


# SET UP OF PYGAME, MOUSE CURSOR & WINDOW:
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Revaniv's Tower")
pygame.mouse.set_visible(True)

# Set up the fonts.
font = pygame.font.Font('Assets/fette-unz-fraktur.ttf', 30)


# SET UP OF THE SPRITES:
class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite


# The different screens of the game:
StartScreen = pygame.image.load("Assets/main_menu.png")
scenario = pygame.image.load("Assets/scenario.png")
tutorial = pygame.image.load("Assets/tutoriel.png")
GameOverScreen1 = pygame.image.load("Assets/game_over_screen1.png")
GameOverScreen2 = pygame.image.load("Assets/game_over_screen2.png")
Win_screen = pygame.image.load("Assets/Win_screen.png")

logo = pygame.image.load('Assets/logo_icon.ico')
pygame.display.set_icon(logo)

# Sprites of the characters:
player = pygame.image.load("Assets/core_character_right_1.png")
player_2 = pygame.image.load("Assets/core_character_left.png")
run_right_list = [pygame.image.load("Assets/core_character_run_right_1.png"),
                  pygame.image.load("Assets/core_character_run_right_2.png"),
                  pygame.image.load("Assets/core_character_run_right_3.png"),
                  pygame.image.load("Assets/core_character_run_right_4.png"),
                  pygame.image.load("Assets/core_character_run_right_5.png"),
                  pygame.image.load("Assets/core_character_run_right_6.png")]
playerRect = pygame.Rect(0, 541, 25, 49)
baddie = pygame.image.load(("Assets/skin_sorcier_revaniv.png"))
badRect = pygame.Rect(50, 180, 50, 50)

# Sprites of the objects:
tomato1 = pygame.image.load("Assets/tomato.png")
tomato1rect = pygame.Rect(50, 190, 15, 15)
tomato2 = pygame.image.load("Assets/tomato.png")
tomato2rect = pygame.Rect(50, 190, 15, 15)
tomato3 = pygame.image.load("Assets/tomato.png")
tomato3rect = pygame.Rect(50, 190, 15, 15)
bg = pygame.image.load("Assets/map_cantine.jpeg")
potion = pygame.image.load("Assets/potion.png")
potionrect = pygame.Rect(600, 600, 17, 28)
beer = pygame.image.load("Assets/beer.png")
beerrect = pygame.Rect(600, 600, 25, 23)

# SET UP OF THE MUSIC:
StartJingle = pygame.mixer.Sound("Assets/StartJingle.wav")
pygame.mixer.music.load('Assets/background.wav')
HitSound = pygame.mixer.Sound('Assets/hit_sound.wav')
GameOverSound = pygame.mixer.Sound('Assets/gameover.mp3')
TimeRun = pygame.mixer.Sound("Assets/run_time.mp3")
WinSound = pygame.mixer.Sound("Assets/win_sound.mp3")
potionSound = pygame.mixer.Sound("Assets/potion.mp3")


# ------------------------------------------------------------------------------------


# FUNCTIONS:

def terminate():  # Shut down the game & close the window.
    pygame.quit()
    sys.exit()


def waitForPlayerToPressKey():  # Locks the screen until the player press a key.
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # Pressing ESC quits.
                    terminate()
                return


def redrawScreen():  # Update the screen, including by redrawing the sprites & the texts.
    windowSurface.blit(bg, (0, 0))
    windowSurface.blit(player, playerRect)
    windowSurface.blit(baddie, badRect)
    windowSurface.blit(tomato1, tomato1rect)
    windowSurface.blit(tomato2, tomato2rect)
    windowSurface.blit(tomato3, tomato3rect)
    windowSurface.blit(potion, potionrect)
    windowSurface.blit(beer, beerrect)
    pygame.draw.rect(windowSurface, BLUE, P1)
    pygame.draw.rect(windowSurface, BLUE, P2)
    pygame.draw.rect(windowSurface, BLUE, P3)
    pygame.draw.rect(windowSurface, BLUE, P4)
    drawText('Health: %s' % (HEALTH), font, windowSurface, WHITE, 10, 10)
    drawText("Time Score: %s" % (BONUS), font, windowSurface, WHITE, 10, 45)
    pygame.display.flip()
    windowSurface.fill(WHITE)


def y_trajectory(y_basis, y_speed, t):  # Calculates the vertical trajectory of the object.
    y = y_basis - ((-9.81 / 30) * (t ** 2) / 2 + y_speed * t)
    return y


def beer_x_speed(player_x):  # Calculates the horizontal velocity of the beer projectile.
    x_speed = (player_x - 60) / 64
    return x_speed


def drawText(text, font, surface, color, x, y):  # Displays texts on the screen.
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def displayScreen(x):
    windowSurface.blit(x, (0, 0))
    pygame.display.update()
    waitForPlayerToPressKey()


def displayWinScreen(x):
    windowSurface.blit(x, (0, 0))
    drawText("%s" % (finalscore), font, windowSurface, WHITE, 335, 110)
    pygame.display.update()
    waitForPlayerToPressKey()


def updateObjects():  # Re-initializes the positions of the objects after an event (win / loose).
    playerRect.update(0, 541, 25, 49)
    badRect.update(50, 180, 50, 50)
    tomato1rect.update(50, 190, 15, 15)
    tomato2rect.update(50, 190, 15, 15)
    tomato3rect.update(50, 190, 15, 15)
    beerrect.update(600, 600, 25, 23)


def initGame():  # Sets up the Start screens of the game:
    displayScreen(scenario)
    StartJingle.play()
    time.sleep(0.5)
    displayScreen(StartScreen)
    time.sleep(0.5)
    displayScreen(tutorial)
    time.sleep(0.5)


# ------------------------------------------------------------------------------------


# MAIN LOOP OF THE GAME:

# It contains the movements of the players (horizontal displacement, jumping, platforms),
# the behaviour of the projectiles and the win / loose events.


initGame()
musicPlaying = True
running = True

while running:

    moveLeft = moveRight = False
    pygame.mixer.music.play(-1, 0.0, 3000)

    while True:

        # GETS & PERFORMS AN ACTION FOR EACH PYGAME EVENT OCCURRING:

        for event in pygame.event.get():
            if event.type == QUIT:
                # Closes the game
                running = False
                terminate()

            if event.type == KEYDOWN:  # Gets & performs an action for each key pressed DOWN:

                if event.key == K_LEFT or event.key == K_a:
                    # Left key = left movement
                    moveRight = False
                    moveLeft = True
                    player = pygame.image.load("Assets/core_character_run_left.png")
                if event.key == K_RIGHT or event.key == K_d:
                    # Right key = right movement
                    moveLeft = False
                    moveRight = True
                    player = run_right_list[0]

                if event.key == K_SPACE and isJump == False:
                    # Space bar = Jump
                    if event.key == K_LEFT or event.key == K_a:
                        player = pygame.image.load("Assets/core_character_jump_left.png")
                    elif event.key == K_RIGHT or event.key == K_d:
                        player = pygame.image.load("Assets/core_character_jump_right.png")
                    isJump = True
                    t = 0
                    y_basis = playerRect.y
                    y_speed = PLAYERMOVERATE_Y

            if event.type == KEYUP:  # Gets & performs an action for each key pressed UP:
                if event.key == K_ESCAPE:
                    # ESC = shuts down the game
                    running = False
                    terminate()

                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                    player = pygame.image.load("Assets/core_character_left.png")
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                    player = pygame.image.load("Assets/core_character_right_1.png")

                if event.key == K_m:
                    # M key = mutes the background music
                    if musicPlaying:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                    musicPlaying = not musicPlaying

        # --------------------------------------

        # PLAYER'S MOVEMENTS:
        if moveLeft and playerRect.left > 0:
            playerRect.left -= PLAYERMOVERATE_X
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.right += PLAYERMOVERATE_X

        # JUMPING MECHANICS & COLLISIONS WITH PLATFORMS:
        if isJump:
            playerRect.y = y_trajectory(y_basis, y_speed, t)
            t += 1

            if playerRect.colliderect(P1):
                if playerRect.y > P1_Y:
                    y_speed = 0
                    t = 0
                    y_basis = playerRect.y + 10
                elif playerRect.y <= P1_Y:
                    isJump = False
                    playerRect.y = P1_Y - 50
                    isOnP1 = True
                if P1_Y + P_Y > playerRect.y > P1_Y - 49:
                    isOnP1 = False

            if playerRect.colliderect(P2):
                if playerRect.y > P2_Y:
                    y_speed = 0
                    t = 0
                    y_basis = playerRect.y + 10
                elif playerRect.y <= P2_Y:
                    isJump = False
                    playerRect.y = P2_Y - 50
                    isOnP2 = True
                if P2_Y + P_Y > playerRect.y > P2_Y - 49:
                    isOnP2 = False

            if playerRect.colliderect(P3):
                if playerRect.y > P3_Y:
                    y_speed = 0
                    t = 0
                    y_basis = playerRect.y + 10
                elif playerRect.y <= P3_Y:
                    isJump = False
                    playerRect.y = P3_Y - 50
                    isOnP3 = True
                if P3_Y + P_Y > playerRect.y > P3_Y - 49:
                    isOnP3 = False

            if playerRect.colliderect(P4):
                if playerRect.y > P4_Y:
                    y_speed = 0
                    t = 0
                    y_basis = playerRect.y + 10
                elif playerRect.y <= P4_Y:
                    isJump = False
                    playerRect.y = P4_Y - 50
                    isOnP4 = True
                if P4_Y + P_Y > playerRect.y > P4_Y - 49:
                    isOnP4 = False

        if isOnP1 and not (P1_X - 25 < playerRect.x < P1_X + P1_LX):
            isOnP1 = False
            isJump = True
            y_speed = 0
            y_basis = playerRect.y
            t = 0

        if isOnP2 and not (P2_X - 25 < playerRect.x < P2_X + P2_LX):
            isOnP2 = False
            isJump = True
            y_speed = 0
            y_basis = playerRect.y
            t = 0

        if isOnP3 and not (P3_X - 25 < playerRect.x < P3_X + P3_LX):
            isOnP3 = False
            isJump = True
            y_speed = 0
            y_basis = playerRect.y
            t = 0

        if isOnP4 and not (P4_X - 25 < playerRect.x < P4_X + P4_LX):
            isOnP4 = False
            isJump = True
            y_speed = 0
            y_basis = playerRect.y
            t = 0


        # --------------------------------------

        # MECHANICS OF THE BEER PROJECTILE:
        if (not beer_launched) and playerRect.y < P4_Y and beer_cooldown == 0:
            beerrect.x = 60
            beerrect.y = 180
            beer_x = beer_x_speed(playerRect.x)
            beer_launched = True
            t_beer = 0

        if beer_launched and not (0 < beerrect.x < 575):
            beer_x = -beer_x

        if beer_launched and (beerrect.colliderect(P3) or beerrect.colliderect(P4)):
            beer_launched = False
            beer_x = 0
            beerrect.x = beerrect.y = 600
            beer_cooldown = 60

        if beer_launched:
            beerrect.y = y_trajectory(180, 10, t_beer)
            beerrect.x += beer_x
            t_beer += 1
        if not (beer_launched) and beer_cooldown > 0:
            beer_cooldown -= 1

        # --------------------------------------

        # MECHANICS OF THE TOMATOES PROJECTILE:
        tomato1rect.x += tomato1moverate
        if (not (585 >= tomato1rect.x >= 0) and tomato1rect.y < 550) or (tomato1rect.y > 550 and tomato1rect.x >= 585):
            tomato1rect.x -= tomato1moverate
            tomato1moverate = -tomato1moverate
        if not (tomato1rect.colliderect(P1) or tomato1rect.colliderect(P2) or tomato1rect.colliderect(
                P3) or tomato1rect.colliderect(P4)) and not tomato1jump:
            tomato1jump = True
            tomato1_y_basis = tomato1rect.y
            t_tomato1 = 0
        if (tomato1rect.colliderect(P1) or tomato1rect.colliderect(P2) or tomato1rect.colliderect(
                P3) or tomato1rect.colliderect(P4)) and tomato1jump:
            tomato1jump = False
            tomato1rect.y -= 10

        if tomato1jump:
            tomato1rect.y = y_trajectory(tomato1_y_basis, 0, t_tomato1)
            t_tomato1 += 1

        tomato2rect.x += tomato2moverate
        if (not (585 >= tomato2rect.x >= 0) and tomato2rect.y < 550) or (tomato2rect.y > 550 and tomato2rect.x >= 585):
            tomato2rect.x -= tomato2moverate
            tomato2moverate = -tomato2moverate
        if not (tomato2rect.colliderect(P1) or tomato2rect.colliderect(P2) or tomato2rect.colliderect(
                P3) or tomato2rect.colliderect(P4)) and not tomato2jump:
            tomato2jump = True
            tomato2_y_basis = tomato2rect.y
            t_tomato2 = 0
        if (tomato2rect.colliderect(P1) or tomato2rect.colliderect(P2) or tomato2rect.colliderect(
                P3) or tomato2rect.colliderect(P4)) and tomato2jump:
            tomato2jump = False
            tomato2rect.y -= 10

        if tomato2jump:
            tomato2rect.y = y_trajectory(tomato2_y_basis, 0, t_tomato2)
            t_tomato2 += 1

        tomato3rect.x += tomato3moverate
        if (not (585 >= tomato3rect.x >= 0) and tomato3rect.y < 550) or (tomato3rect.y > 550 and tomato3rect.x >= 585):
            tomato3rect.x -= tomato3moverate
            tomato3moverate = -tomato3moverate
        if not (tomato3rect.colliderect(P1) or tomato3rect.colliderect(P2) or tomato3rect.colliderect(
                P3) or tomato3rect.colliderect(P4)) and not tomato3jump:
            tomato3jump = True
            tomato3_y_basis = tomato3rect.y
            t_tomato3 = 0
        if (tomato3rect.colliderect(P1) or tomato3rect.colliderect(P2) or tomato3rect.colliderect(
                P3) or tomato3rect.colliderect(P4)) and tomato3jump:
            tomato3jump = False
            tomato3rect.y -= 10

        if tomato3jump:
            tomato3rect.y = y_trajectory(tomato3_y_basis, 0, t_tomato3)
            t_tomato3 += 1


        # Timing tomatoes' movement + potion's appearance:
        timer += 1

        if timer == 60:
            tomato1moverate = 4
        if timer == 260:
            tomato2moverate = 4
        if timer == 460:
            tomato3moverate = 4
        if timer == 700 and potion_checked == True:
            potionrect.x = randint(50, 420)
            potionrect.y = 440
        if timer < 700 and potion_checked == True:
            potionrect.x = 600
            potionrect.y = 600

        # When the player takes the potion:
        if playerRect.colliderect(potionrect) and potion_checked == True:
            potionSound.play()
            potionrect.x = 600
            potionrect.y = 600
            HEALTH += 1
            potion_checked = False

        if tomato1rect.y > 500 and tomato1rect.x < -15:
            tomato1rect.x = 50
            tomato1rect.y = 190
            tomato1jump = False
            tomato1moverate = -tomato1moverate
        if tomato2rect.y > 500 and tomato2rect.x < -15:
            tomato2rect.x = 50
            tomato2rect.y = 190
            tomato2jump = False
            tomato2moverate = -tomato2moverate
        if tomato3rect.y > 500 and tomato3rect.x < -15:
            tomato3rect.x = 50
            tomato3rect.y = 190
            tomato3jump = False
            tomato3moverate = -tomato3moverate


        # --------------------------------------

        # LOOSES & WINS EVENTS:

        # Time Score's functioning:
        bonus_cpt += 1
        if bonus_cpt > 150:
            BONUS -= 100
            bonus_cpt = 0
        if BONUS == 1000:  # Warning when time is running out:
            pygame.mixer.music.stop()
            TimeRun.set_volume(0.5)
            TimeRun.play()
            pygame.mixer.music.play(-1, 0.0, 3000)


        # GAME OVER:
        if HEALTH == 0:
            pygame.mixer.music.stop()
            GameOverSound.play()
            if death[0] > death[1]:
                displayScreen(GameOverScreen1)  # Death by projectiles
            else:
                displayScreen(GameOverScreen2)  # Death by time
            waitForPlayerToPressKey()
            pygame.mixer.music.stop()
            tomato1moverate = tomato2moverate = tomato3moverate = 0
            timer = t_beer = beer_cooldown = 0
            beer_x = 0
            HEALTH = 3
            BONUS = 5000
            bonus_cpt = 0
            isJump = False
            beer_launched = False
            potion_checked = True
            finalscore = 0
            updateObjects()
            initGame()
            pygame.mixer.music.play(-1, 0.0, 3000)


        # HIT BY PROJECTILES:
        if playerRect.colliderect(tomato1rect) or playerRect.colliderect(tomato2rect) or playerRect.colliderect(
                tomato3rect) or playerRect.colliderect(beerrect):
            tomato1jump = tomato2jump = tomato3jump = False
            pygame.mixer.music.stop()
            HitSound.play()
            waitForPlayerToPressKey()
            updateObjects()
            isJump = False
            beer_launched = False
            tomato1moverate = tomato2moverate = tomato3moverate = 0
            timer = 0
            moveLeft = moveRight = False
            HitSound.stop()
            pygame.mixer.music.play(-1, 0.0, 3000)
            HEALTH -= 1
            BONUS = 5000
            death[0] += 1


        # ELAPSED TIME:
        if BONUS == -100:
            tomato1jump = tomato2jump = tomato3jump = False
            pygame.mixer.music.stop()
            HitSound.play()
            waitForPlayerToPressKey()
            updateObjects()
            isJump = False
            beer_launched = False
            tomato1moverate = tomato2moverate = tomato3moverate = 0
            timer = 0
            moveLeft = moveRight = False
            HitSound.stop()
            pygame.mixer.music.play(-1, 0.0, 3000)
            HEALTH -= 1
            BONUS = 5000
            death[1] += 1


        # VICTORY:
        if playerRect.colliderect(badRect):
            moveLeft = moveRight = False
            tomato1moverate = tomato2moverate = tomato3moverate = 0
            tomato1jump = tomato2jump = tomato3jump = False
            finalscore = BONUS + 1000 * HEALTH
            pygame.mixer.music.stop()
            WinSound.play()
            displayWinScreen(Win_screen)
            waitForPlayerToPressKey()
            pygame.mixer.music.stop()
            tomato1moverate = tomato2moverate = tomato3moverate = 0
            timer = t_beer = beer_cooldown = 0
            beer_x = 0
            HEALTH = 3
            BONUS = 5000
            bonus_cpt = 0
            isJump = False
            beer_launched = False
            potion_checked = True
            finalscore = 0
            updateObjects()
            initGame()
            pygame.mixer.music.play(-1, 0.0, 3000)

        redrawScreen()
        mainClock.tick(FPS)
