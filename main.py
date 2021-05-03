import pygame, sys, time
from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 2, 512)

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
BONUS = 1100
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

# Set up the fonts.
font = pygame.font.Font('Assets/fette-unz-fraktur.ttf', 30)


# Set up images.

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite


StartScreen = pygame.image.load("Assets/main_menu.png")
scenario = pygame.image.load("Assets/scenario.png")
tutorial = pygame.image.load("Assets/tutoriel.png")
GameOverScreen = pygame.image.load("Assets/game_over_screen.png")
logo = pygame.image.load('Assets/logoicon.ico')
Win_screen = pygame.image.load("Assets/Win_screen.png")

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
tomato1 = pygame.image.load("Assets/tomato.png")
tomato1rect = pygame.Rect(50, 190, 15, 15)
tomato2 = pygame.image.load("Assets/tomato.png")
tomato2rect = pygame.Rect(50, 190, 15, 15)
tomato3 = pygame.image.load("Assets/tomato.png")
tomato3rect = pygame.Rect(50, 190, 15, 15)
bg = pygame.image.load("Assets/map_cantine.jpeg")

# Set up music.
StartJingle = pygame.mixer.Sound("Assets/StartJingle.wav")
pygame.mixer.music.load('Assets/background.wav')
HitSound = pygame.mixer.Sound('Assets/hit_sound.wav')
GameOverSound = pygame.mixer.Sound('Assets/gameover.wav')
TimeRun = pygame.mixer.Sound("Assets/run_time.mp3")
WinSound = pygame.mixer.Sound("Assets/win_sound.mp3")


# Functions:

def terminate():
    pygame.quit()
    sys.exit()


def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # Pressing ESC quits.
                    terminate()
                return


def redrawScreen():
    windowSurface.blit(bg, (0, 0))
    windowSurface.blit(player, playerRect)
    windowSurface.blit(baddie, badRect)
    windowSurface.blit(tomato1, tomato1rect)
    windowSurface.blit(tomato2, tomato2rect)
    windowSurface.blit(tomato3, tomato3rect)
    pygame.draw.rect(windowSurface, BLUE, P1)
    pygame.draw.rect(windowSurface, BLUE, P2)
    pygame.draw.rect(windowSurface, BLUE, P3)
    pygame.draw.rect(windowSurface, BLUE, P4)
    drawText('Health: %s' % (HEALTH), font, windowSurface, WHITE, 10, 10)
    drawText("Time Score: %s" % (BONUS), font, windowSurface, WHITE, 10, 45)
    pygame.display.flip()
    windowSurface.fill(WHITE)


def y_trajectory(y_basis, y_speed, t):
    y = y_basis - ((-9.81 / 30) * t ** 2 / 2 + y_speed * t)
    return y


def drawText(text, font, surface, color, x, y):
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
    drawText("%s" %(finalscore), font, windowSurface, BLUE, 400, 500)
    pygame.display.update()
    waitForPlayerToPressKey()


# Set up the Start screen of the game:
displayScreen(scenario)
StartJingle.play()
displayScreen(StartScreen)
displayScreen(tutorial)
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
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                    player = pygame.image.load("Assets/core_character_run_left.png")
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                    player = run_right_list[0]
                if event.key == K_SPACE and isJump == False:
                    if event.key == K_LEFT or event.key == K_a:
                        player = pygame.image.load("Assets/core_character_jump_left.png")
                    elif event.key == K_RIGHT or event.key == K_d:
                        player = pygame.image.load("Assets/core_character_jump_right.png")
                    isJump = True
                    t = 0
                    y_basis = playerRect.y
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
                    terminate()

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
        if moveLeft and playerRect.left > 0:
            playerRect.left -= PLAYERMOVERATE_X
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.right += PLAYERMOVERATE_X

        # if isJump is True:
        #    playerRect.y -= PLAYERMOVERATE_Y * 2
        #    PLAYERMOVERATE_Y -= 1
        #    if PLAYERMOVERATE_Y < -10:
        #        isJump = False
        #        PLAYERMOVERATE_Y = 10

        # Jump mechanics
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

        # if badLeft and badRect.left > 0:
        # badRight = False
        # badRect.left -= BADDIEMOVERATE
        # if badRight and badRect.right < WINDOWWIDTH:
        # badLeft = False
        # badRect.right += BADDIEMOVERATE

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

        tomato_timer += 1

        if tomato_timer == 60:
            tomato1moverate = 4
        if tomato_timer == 260:
            tomato2moverate = 4
        if tomato_timer == 460:
            tomato3moverate = 4

        if (tomato1rect.y > 500 and tomato1rect.x < -15):
            tomato1rect.x = 50
            tomato1rect.y = 190
            tomato1jump = False
            tomato1moverate = -tomato1moverate
        if (tomato2rect.y > 500 and tomato2rect.x < -15):
            tomato2rect.x = 50
            tomato2rect.y = 190
            tomato2jump = False
            tomato2moverate = -tomato2moverate
        if (tomato3rect.y > 500 and tomato3rect.x < -15):
            tomato3rect.x = 50
            tomato3rect.y = 190
            tomato3jump = False
            tomato3moverate = -tomato3moverate

        if HEALTH == 0:
            GameOverSound.play()
            displayScreen(GameOverScreen)
            waitForPlayerToPressKey()
            terminate()

        bonus_cpt += 1
        if bonus_cpt > 150:
            BONUS -= 100
            bonus_cpt = 0
        if BONUS == 1000:
            pygame.mixer.music.stop()
            TimeRun.set_volume(0.5)
            TimeRun.play()
            pygame.mixer.music.play(-1, 0.0, 3000)
        #while BONUS <= 1000:
            #drawText("Time Score: %s" % (BONUS), font, windowSurface, RED, 10, 45)
        if BONUS < 0:
            BONUS = 0

        if playerRect.colliderect(tomato1rect) or playerRect.colliderect(tomato2rect) or playerRect.colliderect(
                tomato3rect) or BONUS == 0:
            tomato1jump = tomato2jump = tomato3jump = False
            pygame.mixer.music.stop()
            HitSound.play()
            waitForPlayerToPressKey()
            playerRect.update(0, 541, 25, 49)
            isJump = False
            badRect.update(50, 180, 50, 50)
            tomato1rect.update(50, 190, 15, 15)
            tomato2rect.update(50, 190, 15, 15)
            tomato3rect.update(50, 190, 15, 15)
            tomato1moverate = tomato2moverate = tomato3moverate = 0
            tomato_timer = 0
            moveLeft = moveRight = False
            HitSound.stop()
            pygame.mixer.music.play(-1, 0.0, 3000)
            HEALTH -= 1
            BONUS = 5000

        if playerRect.colliderect(badRect):
            moveLeft = moveRight = False
            tomato1moverate = tomato2moverate = tomato3moverate = 0
            tomato1jump = tomato2jump = tomato3jump = False
            finalscore = BONUS + 1000*HEALTH
            pygame.mixer.music.stop()
            WinSound.play()
            displayWinScreen(Win_screen)
            waitForPlayerToPressKey()
            terminate()

        redrawScreen()
        mainClock.tick(FPS)
