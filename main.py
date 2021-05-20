import pygame, sys, time
from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
import assets as ast
import constants as cst
import functions as fc

# CONSTANTS

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((cst.WINDOWWIDTH, cst.WINDOWHEIGHT))
pygame.display.set_caption("Revaniv's Tower")
pygame.mouse.set_visible(True)

# ASSETS





# Functions:




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
                if event.key == K_SPACE and cst.isJump == False:
                    if event.key == K_LEFT or event.key == K_a:
                        player = pygame.image.load("Assets/core_character_jump_left.png")
                    elif event.key == K_RIGHT or event.key == K_d:
                        player = pygame.image.load("Assets/core_character_jump_right.png")
                    cst.isJump = True
                    t = 0
                    y_basis = ast.playerRect.y
                    y_speed = cst.PLAYERMOVERATE_Y

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
            ast.playerRect.left -= cst.PLAYERMOVERATE_X
        if moveRight and ast.playerRect.right < cst.WINDOWWIDTH:
            ast.playerRect.right += cst.PLAYERMOVERATE_X

        # if isJump is True:
        #    playerRect.y -= PLAYERMOVERATE_Y * 2
        #    PLAYERMOVERATE_Y -= 1
        #    if PLAYERMOVERATE_Y < -10:
        #        isJump = False
        #        PLAYERMOVERATE_Y = 10

        # Jump mechanics
        if cst.isJump:
            ast.playerRect.y = fc.y_trajectory(y_basis, y_speed, t)
            t += 1

            if ast.playerRect.colliderect(cst.P1):
                if ast.playerRect.y > cst.P1_Y:
                    y_speed = 0
                    t = 0
                    y_basis = ast.playerRect.y + 10
                elif ast.playerRect.y <= cst.P1_Y:
                    cst.isJump = False
                    ast.playerRect.y = cst.P1_Y - 50
                    cst.isOnP1 = True
                if cst.P1_Y + cst.P_Y > ast.playerRect.y > cst.P1_Y - 49:
                    cst.isOnP1 = False

            if ast.playerRect.colliderect(cst.P2):
                if ast.playerRect.y > cst.P2_Y:
                    y_speed = 0
                    t = 0
                    y_basis = ast.playerRect.y + 10
                elif ast.playerRect.y <= cst.P2_Y:
                    cst.isJump = False
                    ast.playerRect.y = cst.P2_Y - 50
                    cst.isOnP2 = True
                if cst.P2_Y + cst.P_Y > ast.playerRect.y > cst.P2_Y - 49:
                    cst.isOnP2 = False

            if ast.playerRect.colliderect(cst.P3):
                if ast.playerRect.y > cst.P3_Y:
                    y_speed = 0
                    t = 0
                    y_basis = ast.playerRect.y + 10
                elif ast.playerRect.y <= cst.P3_Y:
                    cst.isJump = False
                    ast.playerRect.y = cst.P3_Y - 50
                    cst.isOnP3 = True
                if cst.P3_Y + cst.P_Y > ast.playerRect.y > cst.P3_Y - 49:
                    cst.isOnP3 = False

            if ast.playerRect.colliderect(cst.P4):
                if ast.playerRect.y > cst.P4_Y:
                    y_speed = 0
                    t = 0
                    y_basis = ast.playerRect.y + 10
                elif ast.playerRect.y <= cst.P4_Y:
                    cst.isJump = False
                    ast.playerRect.y = cst.P4_Y - 50
                    cst.isOnP4 = True
                if cst.P4_Y + cst.P_Y > ast.playerRect.y > cst.P4_Y - 49:
                    cst.isOnP4 = False

        if cst.isOnP1 and not (cst.P1_X - 25 < ast.playerRect.x < cst.P1_X + cst.P1_LX):
            cst.isOnP1 = False
            cst.isJump = True
            y_speed = 0
            y_basis = ast.playerRect.y
            t = 0

        if cst.isOnP2 and not (cst.P2_X - 25 < ast.playerRect.x < cst.P2_X + cst.P2_LX):
            cst.isOnP2 = False
            cst.isJump = True
            y_speed = 0
            y_basis = ast.playerRect.y
            t = 0

        if cst.isOnP3 and not (cst.P3_X - 25 < ast.playerRect.x < cst.P3_X + cst.P3_LX):
            cst.isOnP3 = False
            cst.isJump = True
            y_speed = 0
            y_basis = ast.playerRect.y
            t = 0

        if cst.isOnP4 and not (cst.P4_X - 25 < ast.playerRect.x < cst.P4_X + cst.P4_LX):
            cst.isOnP4 = False
            cst.isJump = True
            y_speed = 0
            y_basis = ast.playerRect.y
            t = 0

        # if badLeft and badRect.left > 0:
        # badRight = False
        # badRect.left -= BADDIEMOVERATE
        # if badRight and badRect.right < WINDOWWIDTH:
        # badLeft = False
        # badRect.right += BADDIEMOVERATE

        ast.tomato1rect.x += cst.tomato1moverate
        if (not (585 >= ast.tomato1rect.x >= 0) and ast.tomato1rect.y < 550) or (ast.tomato1rect.y > 550 and ast.tomato1rect.x >= 585):
            ast.tomato1rect.x -= cst.tomato1moverate
            cst.tomato1moverate = -cst.tomato1moverate
        if not (ast.tomato1rect.colliderect(cst.P1) or ast.tomato1rect.colliderect(cst.P2) or ast.tomato1rect.colliderect(
                cst.P3) or ast.tomato1rect.colliderect(cst.P4)) and not cst.tomato1jump:
            cst.tomato1jump = True
            tomato1_y_basis = ast.tomato1rect.y
            t_tomato1 = 0
        if (ast.tomato1rect.colliderect(cst.P1) or ast.tomato1rect.colliderect(cst.P2) or ast.tomato1rect.colliderect(
                cst.P3) or ast.tomato1rect.colliderect(cst.P4)) and cst.tomato1jump:
            tomato1jump = False
            ast.tomato1rect.y -= 10

        if cst.tomato1jump:
            ast.tomato1rect.y = fc.y_trajectory(tomato1_y_basis, 0, t_tomato1)
            t_tomato1 += 1

        ast.tomato2rect.x += cst.tomato2moverate
        if (not (585 >= ast.tomato2rect.x >= 0) and ast.tomato2rect.y < 550) or (ast.tomato2rect.y > 550 and ast.tomato2rect.x >= 585):
            ast.tomato2rect.x -= cst.tomato2moverate
            cst.tomato2moverate = -cst.tomato2moverate
        if not (ast.tomato2rect.colliderect(cst.P1) or ast.tomato2rect.colliderect(cst.P2) or ast.tomato2rect.colliderect(
                cst.P3) or ast.tomato2rect.colliderect(cst.P4)) and not cst.tomato2jump:
            cst.tomato2jump = True
            tomato2_y_basis = ast.tomato2rect.y
            t_tomato2 = 0
        if (ast.tomato2rect.colliderect(cst.P1) or ast.tomato2rect.colliderect(cst.P2) or ast.tomato2rect.colliderect(
                cst.P3) or ast.tomato2rect.colliderect(cst.P4)) and cst.tomato2jump:
            cst.tomato2jump = False
            ast.tomato2rect.y -= 10

        if cst.tomato2jump:
            ast.tomato2rect.y = fc.y_trajectory(tomato2_y_basis, 0, t_tomato2)
            t_tomato2 += 1

        ast.tomato3rect.x += cst.tomato3moverate
        if (not (585 >= ast.tomato3rect.x >= 0) and ast.tomato3rect.y < 550) or (ast.tomato3rect.y > 550 and ast.tomato3rect.x >= 585):
            ast.tomato3rect.x -= cst.tomato3moverate
            cst.tomato3moverate = -cst.tomato3moverate
        if not (ast.tomato3rect.colliderect(cst.P1) or ast.tomato3rect.colliderect(cst.P2) or ast.tomato3rect.colliderect(
                cst.P3) or ast.tomato3rect.colliderect(cst.P4)) and not cst.tomato3jump:
            cst.tomato3jump = True
            tomato3_y_basis = ast.tomato3rect.y
            t_tomato3 = 0
        if (ast.tomato3rect.colliderect(cst.P1) or ast.tomato3rect.colliderect(cst.P2) or ast.tomato3rect.colliderect(
                cst.P3) or ast.tomato3rect.colliderect(cst.P4)) and cst.tomato3jump:
            tomato3jump = False
            ast.tomato3rect.y -= 10

        if cst.tomato3jump:
            ast.tomato3rect.y = fc.y_trajectory(tomato3_y_basis, 0, t_tomato3)
            t_tomato3 += 1

        cst.tomato_timer += 1

        if cst.tomato_timer == 60:
            tomato1moverate = 4
        if cst.tomato_timer == 260:
            tomato2moverate = 4
        if cst.tomato_timer == 460:
            tomato3moverate = 4

        if (ast.tomato1rect.y > 500 and ast.tomato1rect.x < -15):
            ast.tomato1rect.x = 50
            ast.tomato1rect.y = 190
            tomato1jump = False
            tomato1moverate = -cst.tomato1moverate
        if (ast.tomato2rect.y > 500 and ast.tomato2rect.x < -15):
            ast.tomato2rect.x = 50
            ast.tomato2rect.y = 190
            tomato2jump = False
            tomato2moverate = -cst.tomato2moverate
        if (ast.tomato3rect.y > 500 and ast.tomato3rect.x < -15):
            ast.tomato3rect.x = 50
            ast.tomato3rect.y = 190
            tomato3jump = False
            tomato3moverate = -cst.tomato3moverate

        if cst.HEALTH == 0:
            pygame.mixer.music.stop()
            ast.GameOverSound.play()
            fc.displayScreen(ast.GameOverScreen)
            fc.waitForPlayerToPressKey()
            fc.terminate()

        cst.bonus_cpt += 1
        if cst.bonus_cpt > 150:
            cst.BONUS -= 100
            cst.bonus_cpt = 0
        if cst.BONUS == 1000:
            pygame.mixer.music.stop()
            ast.TimeRun.set_volume(0.5)
            ast.TimeRun.play()
            pygame.mixer.music.play(-1, 0.0, 3000)
        if cst.BONUS < 0:
            cst.BONUS = 0

        if ast.playerRect.colliderect(ast.tomato1rect) or ast.playerRect.colliderect(ast.tomato2rect) or ast.playerRect.colliderect(
                ast.tomato3rect) or cst.BONUS == 0:
            cst.tomato1jump = cst.tomato2jump = cst.tomato3jump = False
            pygame.mixer.music.stop()
            ast.HitSound.play()
            fc.waitForPlayerToPressKey()
            ast.playerRect.update(0, 541, 25, 49)
            cst.isJump = False
            ast.badRect.update(50, 180, 50, 50)
            ast.tomato1rect.update(50, 190, 15, 15)
            ast.tomato2rect.update(50, 190, 15, 15)
            ast.tomato3rect.update(50, 190, 15, 15)
            cst.tomato1moverate = cst.tomato2moverate = cst.tomato3moverate = 0
            cst.tomato_timer = 0
            moveLeft = moveRight = False
            ast.HitSound.stop()
            pygame.mixer.music.play(-1, 0.0, 3000)
            cst.HEALTH -= 1
            BONUS = 5000

        if ast.playerRect.colliderect(ast.badRect):
            moveLeft = moveRight = False
            cst.tomato1moverate = cst.tomato2moverate = cst.tomato3moverate = 0
            cst.tomato1jump = cst.tomato2jump = cst.tomato3jump = False
            cst.finalscore = cst.BONUS + 1000*cst.HEALTH
            pygame.mixer.music.stop()
            ast.WinSound.play()
            fc.displayWinScreen(ast.Win_screen)
            fc.waitForPlayerToPressKey()
            fc.terminate()

        fc.redrawScreen()
        mainClock.tick(cst.FPS)
