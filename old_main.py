import pygame, sys, time
from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
from time import sleep

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
BADDIEMOVERATE = 1

HEALTH = 3
BONUS = 1100
bonus_cpt = 0
isJump = False

# Plateform
P1_X = 50
P1_Y = 440
P1_LX = 200
P_Y = 10
P1 = pygame.Rect(P1_X, P1_Y, P1_LX, P_Y)
isOnP1 = False

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

player = pygame.image.load("Assets/core_character_right_1.png")
player_2 = pygame.image.load("Assets/core_character_left.png")
run_right_list = [pygame.image.load("Assets/core_character_run_right_1.png"),
                  pygame.image.load("Assets/core_character_run_right_2.png"),
                  pygame.image.load("Assets/core_character_run_right_3.png"),
                  pygame.image.load("Assets/core_character_run_right_4.png"),
                  pygame.image.load("Assets/core_character_run_right_5.png"),
                  pygame.image.load("Assets/core_character_run_right_6.png")]
playerRect = pygame.Rect(50, 480, 60, 60)
baddie = pygame.image.load(("Assets/skin_sorcier_revaniv.png"))
badRect = pygame.Rect(500, 480, 50, 50)
bg = pygame.image.load("Assets/map_cantine.jpeg")

# Set up music.
StartJingle = pygame.mixer.Sound("Assets/StartJingle.wav")
pygame.mixer.music.load('Assets/background.wav')
HitSound = pygame.mixer.Sound('Assets/hit_sound.wav')
GameOverSound = pygame.mixer.Sound('Assets/gameover.wav')
TimeRun = pygame.mixer.Sound("Assets/run_time.mp3")


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
    pygame.draw.rect(windowSurface, BLUE, P1)
    drawText('Health: %s' % (HEALTH), font, windowSurface, 10, 10)
    drawText("Time Score: %s" % (BONUS), font, windowSurface, 10, 45)
    pygame.display.flip()
    windowSurface.fill(WHITE)


def y_trajectory(y_basis, y_speed, t):
    y = y_basis - ((-9.81 / 25) * t ** 2 / 2 + y_speed * t)
    return y


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, WHITE)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def drawTextRed(text, font, surface, x, y):
    textobj = font.render(text, 1, RED)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def displayScreen(x):
    windowSurface.blit(x, (0, 0))
    pygame.display.update()
    waitForPlayerToPressKey()


# Set up the Start screen of the game:
# windowSurface.blit(StartScreen, (0, 0))
# StartJingle.play()
# pygame.display.update()
# time.sleep(5)
# waitForPlayerToPressKey()


displayScreen(scenario)
StartJingle.play()
displayScreen(StartScreen)
displayScreen(tutorial)
time.sleep(4.2)

musicPlaying = True
running = True

while running:

    moveLeft = moveRight = False
    badLeft = True
    badRight = False
    pygame.mixer.music.play(-1, 0.0, 5000)

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
                        pygame.mixer.music.play(-1, 0.0, 5000)
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

        if not (playerRect.x > P1_X and playerRect.x < P1_X + P1_LX) and isOnP1 and not isJump:
            isOnP1 = False
            isJump = True
            t = 0
            y_basis = P1_Y - 60
            y_speed = 0

        if isJump:
            if playerRect.y > 485:
                playerRect.y = 480
                t = 0
                y_basis = 480
                isJump = False
            else:
                playerRect.y = y_trajectory(y_basis, y_speed, t)
                t += 1
            if playerRect.x > P1_X and playerRect.x + 60 < P1_X + P1_LX:
                if P1_Y + 5 < playerRect.y < P1_Y + 15:
                    y_speed = 0
                elif playerRect.y + 60 < P1_Y:
                    isOnP1 = True
            else:
                isOnP1 = False
            if isOnP1 and playerRect.y + 60 > P1_Y + 5:
                isJump = False
                playerRect.y = P1_Y - 60

        # if badLeft and badRect.left > 0:
        # badRight = False
        # badRect.left -= BADDIEMOVERATE
        # if badRight and badRect.right < WINDOWWIDTH:
        # badLeft = False
        # badRect.right += BADDIEMOVERATE

        badRect.x -= BADDIEMOVERATE
        if badRect.x <= 0:
            badRect.x += BADDIEMOVERATE
            BADDIEMOVERATE = -BADDIEMOVERATE
        elif badRect.x >= 550:
            badRect.x += BADDIEMOVERATE
            BADDIEMOVERATE = -BADDIEMOVERATE


        bonus_cpt += 1
        if bonus_cpt > 150:
            BONUS -= 100
            bonus_cpt = 0
        if BONUS == 1000:
            pygame.mixer.music.stop()
            TimeRun.set_volume(0.3)
            TimeRun.play()
            pygame.mixer.music.play(-1, 0.0, 5000)
        # while BONUS <= 1000:
        # drawTextRed("Time Score: %s" % (BONUS), font, windowSurface, 10, 45)
        if BONUS < 0:
            BONUS = 0

        if playerRect.colliderect(badRect) or BONUS == 0:
            pygame.mixer.music.stop()
            HitSound.play()
            waitForPlayerToPressKey()
            playerRect.update(50, 480, 50, 50)
            badRect.update(500, 480, 50, 50)
            moveLeft = moveRight = False
            HitSound.stop()
            pygame.mixer.music.play(-1, 0.0, 5000)
            HEALTH -= 1
            playerRect.y = 480
            isOnP1 = False
            BONUS = 5000

        if HEALTH == 0:
            pygame.mixer.music.load('Assets/gameover.wav')
            pygame.mixer.music.play()
            displayScreen(GameOverScreen)
            running = False
            terminate()


        redrawScreen()
        mainClock.tick(FPS)
