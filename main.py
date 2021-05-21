import pygame, sys, time, random
from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
import assets as ast
import functions as fc

# CONSTANTS
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

FPS = 60
PLAYERMOVERATE_X = 4
PLAYERMOVERATE_Y = 10
tomato1moverate = tomato2moverate = tomato3moverate = 0
tomato_timer = 0

HEALTH = 3
BONUS = 4000
bonus_cpt = 0
isJump = False
tomato1jump = tomato2jump = tomato3jump = False
finalscore = 0

# Plateform
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


# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Revaniv's Tower")
pygame.mouse.set_visible(True)

# ASSETS

# FUNCTIONS


# Set up the Start screen of the game:
#fc.waitForPlayerToPressKey() #to rec
fc.displayScreen(ast.scenario)
ast.StartJingle.play()
fc.displayScreen(ast.StartScreen)
fc.displayScreen(ast.tutorial)
time.sleep(3.5)

musicPlaying = True
running = True

while running:

    moveLeft = moveRight = False
    pygame.mixer.music.play(-1, 0.0, 3000)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                fc.terminate()

            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                    player = pygame.image.load("Assets/core_character_run_left.png")
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                    player = ast.run_right_list[0]
                if event.key == K_SPACE and isJump == False:
                    if event.key == K_LEFT or event.key == K_a:
                        player = pygame.image.load("Assets/core_character_jump_left.png")
                    elif event.key == K_RIGHT or event.key == K_d:
                        player = pygame.image.load("Assets/core_character_jump_right.png")
                    isJump = True
                    t = 0
                    y_basis = ast.playerRect.y
                    y_speed = PLAYERMOVERATE_Y

                    # OLD VERSION :
                    # y_basis = playerRect.y
                    # t = 0
                    # playerRect.y = y_trajectory(y_basis, PLAYERMOVERATE_Y, t)
                    # t += 1

            # if isJump and playerRect.y < 500:
            # playerRect.y = y_trajectory(y_basis, PLAYERMOVERATE_Y, t)
            # t += 1
            # if isJump and playerRect.y > 500:
            # isJump = False
            # playerRect.y = 480

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    running = False
                    fc.terminate()

                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                    player = pygame.image.load("Assets/core_character_left.png")
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                    player = pygame.image.load("Assets/core_character_right_1.png")

                if event.key == K_m:
                    if musicPlaying:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                    musicPlaying = not musicPlaying

        # Move the player around.
        if moveLeft and ast.playerRect.left > 0:
            ast.playerRect.left -= PLAYERMOVERATE_X
        if moveRight and ast.playerRect.right < WINDOWWIDTH:
            ast.playerRect.right += PLAYERMOVERATE_X

        # if isJump is True:
        #    playerRect.y -= PLAYERMOVERATE_Y * 2
        #    PLAYERMOVERATE_Y -= 1
        #    if PLAYERMOVERATE_Y < -10:
        #        isJump = False
        #        PLAYERMOVERATE_Y = 10

        # Jump mechanics
        if isJump:
            ast.playerRect.y = fc.y_trajectory(y_basis, y_speed, t)
            t += 1

            if ast.playerRect.colliderect(P1):
                if ast.playerRect.y > P1_Y:
                    y_speed = 0
                    t = 0
                    y_basis = ast.playerRect.y + 10
                elif ast.playerRect.y <= P1_Y:
                    isJump = False
                    ast.playerRect.y = P1_Y - 50
                    isOnP1 = True
                if P1_Y + P_Y > ast.playerRect.y > P1_Y - 49:
                    isOnP1 = False

            if ast.playerRect.colliderect(P2):
                if ast.playerRect.y > P2_Y:
                    y_speed = 0
                    t = 0
                    y_basis = ast.playerRect.y + 10
                elif ast.playerRect.y <= P2_Y:
                    isJump = False
                    ast.playerRect.y = P2_Y - 50
                    isOnP2 = True
                if P2_Y + P_Y > ast.playerRect.y > P2_Y - 49:
                    isOnP2 = False

            if ast.playerRect.colliderect(P3):
                if ast.playerRect.y > P3_Y:
                    y_speed = 0
                    t = 0
                    y_basis = ast.playerRect.y + 10
                elif ast.playerRect.y <= P3_Y:
                    isJump = False
                    ast.playerRect.y = P3_Y - 50
                    isOnP3 = True
                if P3_Y + P_Y > ast.playerRect.y > P3_Y - 49:
                    isOnP3 = False

            if ast.playerRect.colliderect(P4):
                if ast.playerRect.y > P4_Y:
                    y_speed = 0
                    t = 0
                    y_basis = ast.playerRect.y + 10
                elif ast.playerRect.y <= P4_Y:
                    isJump = False
                    ast.playerRect.y = P4_Y - 50
                    isOnP4 = True
                if P4_Y + P_Y > ast.playerRect.y > P4_Y - 49:
                    isOnP4 = False

        if isOnP1 and not (P1_X - 25 < ast.playerRect.x < P1_X + P1_LX):
            isOnP1 = False
            isJump = True
            y_speed = 0
            y_basis = ast.playerRect.y
            t = 0

        if isOnP2 and not (P2_X - 25 < ast.playerRect.x < P2_X + P2_LX):
            isOnP2 = False
            isJump = True
            y_speed = 0
            y_basis = ast.playerRect.y
            t = 0

        if isOnP3 and not (P3_X - 25 < ast.playerRect.x < P3_X + P3_LX):
            isOnP3 = False
            isJump = True
            y_speed = 0
            y_basis = ast.playerRect.y
            t = 0

        if isOnP4 and not (P4_X - 25 < ast.playerRect.x < P4_X + P4_LX):
            isOnP4 = False
            isJump = True
            y_speed = 0
            y_basis = ast.playerRect.y
            t = 0

        # if badLeft and badRect.left > 0:
        # badRight = False
        # badRect.left -= BADDIEMOVERATE
        # if badRight and badRect.right < WINDOWWIDTH:
        # badLeft = False
        # badRect.right += BADDIEMOVERATE

        ast.tomato1rect.x += tomato1moverate
        if (not (585 >= ast.tomato1rect.x >= 0) and ast.tomato1rect.y < 550) or (ast.tomato1rect.y > 550 and ast.tomato1rect.x >= 585):
            ast.tomato1rect.x -= tomato1moverate
            tomato1moverate = -tomato1moverate
        if not (ast.tomato1rect.colliderect(P1) or ast.tomato1rect.colliderect(P2) or ast.tomato1rect.colliderect(
                P3) or ast.tomato1rect.colliderect(P4)) and not tomato1jump:
            tomato1jump = True
            tomato1_y_basis = ast.tomato1rect.y
            t_tomato1 = 0
        if (ast.tomato1rect.colliderect(P1) or ast.tomato1rect.colliderect(P2) or ast.tomato1rect.colliderect(
                P3) or ast.tomato1rect.colliderect(P4)) and tomato1jump:
            tomato1jump = False
            ast.tomato1rect.y -= 10

        if tomato1jump:
            ast.tomato1rect.y = fc.y_trajectory(tomato1_y_basis, 0, t_tomato1)
            t_tomato1 += 1

        ast.tomato2rect.x += tomato2moverate
        if (not (585 >= ast.tomato2rect.x >= 0) and ast.tomato2rect.y < 550) or (ast.tomato2rect.y > 550 and ast.tomato2rect.x >= 585):
            ast.tomato2rect.x -= tomato2moverate
            tomato2moverate = -tomato2moverate
        if not (ast.tomato2rect.colliderect(P1) or ast.tomato2rect.colliderect(P2) or ast.tomato2rect.colliderect(
                P3) or ast.tomato2rect.colliderect(P4)) and not tomato2jump:
            tomato2jump = True
            tomato2_y_basis = ast.tomato2rect.y
            t_tomato2 = 0
        if (ast.tomato2rect.colliderect(P1) or ast.tomato2rect.colliderect(P2) or ast.tomato2rect.colliderect(
                P3) or ast.tomato2rect.colliderect(P4)) and tomato2jump:
            tomato2jump = False
            ast.tomato2rect.y -= 10

        if tomato2jump:
            ast.tomato2rect.y = fc.y_trajectory(tomato2_y_basis, 0, t_tomato2)
            t_tomato2 += 1

        ast.tomato3rect.x += tomato3moverate
        if (not (585 >= ast.tomato3rect.x >= 0) and ast.tomato3rect.y < 550) or (ast.tomato3rect.y > 550 and ast.tomato3rect.x >= 585):
            ast.tomato3rect.x -= tomato3moverate
            tomato3moverate = -tomato3moverate
        if not (ast.tomato3rect.colliderect(P1) or ast.tomato3rect.colliderect(P2) or ast.tomato3rect.colliderect(
                P3) or ast.tomato3rect.colliderect(P4)) and not tomato3jump:
            tomato3jump = True
            tomato3_y_basis = ast.tomato3rect.y
            t_tomato3 = 0
        if (ast.tomato3rect.colliderect(P1) or ast.tomato3rect.colliderect(P2) or ast.tomato3rect.colliderect(
                P3) or ast.tomato3rect.colliderect(P4)) and tomato3jump:
            tomato3jump = False
            ast.tomato3rect.y -= 10

        if tomato3jump:
            ast.tomato3rect.y = fc.y_trajectory(tomato3_y_basis, 0, t_tomato3)
            t_tomato3 += 1

        tomato_timer += 1

        if tomato_timer == 60:
            tomato1moverate = 4
        if tomato_timer == 260:
            tomato2moverate = 4
        if tomato_timer == 460:
            tomato3moverate = 4

        if (ast.tomato1rect.y > 500 and ast.tomato1rect.x < -15):
            ast.tomato1rect.x = 50
            ast.tomato1rect.y = 190
            tomato1jump = False
            tomato1moverate = -tomato1moverate
        if (ast.tomato2rect.y > 500 and ast.tomato2rect.x < -15):
            ast.tomato2rect.x = 50
            ast.tomato2rect.y = 190
            tomato2jump = False
            tomato2moverate = -tomato2moverate
        if (ast.tomato3rect.y > 500 and ast.tomato3rect.x < -15):
            ast.tomato3rect.x = 50
            ast.tomato3rect.y = 190
            tomato3jump = False
            tomato3moverate = -tomato3moverate

        if HEALTH == 0:
            pygame.mixer.music.stop()
            ast.GameOverSound.play()
            fc.displayScreen(ast.GameOverScreen)
            fc.waitForPlayerToPressKey()
            fc.terminate()

        bonus_cpt += 1
        if bonus_cpt > 150:
            BONUS -= 100
            bonus_cpt = 0
        if BONUS == 1000:
            pygame.mixer.music.stop()
            ast.TimeRun.set_volume(0.5)
            ast.TimeRun.play()
            pygame.mixer.music.play(-1, 0.0, 3000)
        if BONUS < 0:
            BONUS = 0

        if BONUS <= 3700:
            windowSurface.blit(ast.potion, ast.potionRect)
            if ast.playerRect.colliderect(ast.potionRect):
                HEALTH += 1
              


        if ast.playerRect.colliderect(ast.tomato1rect) or ast.playerRect.colliderect(ast.tomato2rect) or ast.playerRect.colliderect(ast.tomato3rect) or BONUS == 0:
            tomato1jump = tomato2jump = tomato3jump = False
            pygame.mixer.music.stop()
            ast.HitSound.play()
            fc.waitForPlayerToPressKey()
            ast.playerRect.update(0, 541, 25, 49)
            isJump = False
            ast.badRect.update(50, 180, 50, 50)
            ast.tomato1rect.update(50, 190, 15, 15)
            ast.tomato2rect.update(50, 190, 15, 15)
            ast.tomato3rect.update(50, 190, 15, 15)
            tomato1moverate = tomato2moverate = tomato3moverate = 0
            tomato_timer = 0
            moveLeft = moveRight = False
            ast.HitSound.stop()
            pygame.mixer.music.play(-1, 0.0, 3000)
            HEALTH -= 1
            BONUS = 5000

        if ast.playerRect.colliderect(ast.badRect):
            moveLeft = moveRight = False
            tomato1moverate = tomato2moverate = tomato3moverate = 0
            tomato1jump = tomato2jump = tomato3jump = False
            finalscore = BONUS + 1000*HEALTH
            pygame.mixer.music.stop()
            ast.WinSound.play()
            fc.displayWinScreen(ast.Win_screen)
            fc.waitForPlayerToPressKey()
            fc.terminate()

        fc.redrawScreen()
        mainClock.tick(FPS)
