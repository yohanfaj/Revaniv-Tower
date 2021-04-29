import pygame, sys, time
from pygame.locals import *
from pygame import mixer
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
BADDIEMOVERATE = 4

HEALTH = 3
BONUS = 5000
bonus_cpt = 0
isJump = False
badJump = False

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
pygame.display.set_caption("Revaniv's Tower - Alpha")
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
logo = pygame.image.load('Assets/logoicon.ico')
player = pygame.image.load("Assets/core_character_right_1.png")
player_2 = pygame.image.load("Assets/core_character_left.png")
run_right_list = [pygame.image.load("Assets/core_character_run_right_1.png"),
                  pygame.image.load("Assets/core_character_run_right_2.png"),
                  pygame.image.load("Assets/core_character_run_right_3.png"),
                  pygame.image.load("Assets/core_character_run_right_4.png"),
                  pygame.image.load("Assets/core_character_run_right_5.png"),
                  pygame.image.load("Assets/core_character_run_right_6.png")]
playerRect = pygame.Rect(50, 480, 25, 49)
baddie = pygame.image.load(("Assets/skin_sorcier_revaniv.png"))
badRect = pygame.Rect(50, 180, 50, 50)
bg = pygame.image.load("Assets/map_cantine.jpeg")

# Set up music.
StartJingle = mixer.Sound("Assets/StartJingle.wav")
mixer.music.load('Assets/background.wav')
HitSound = mixer.Sound('Assets/hit_sound.wav')
GameOverSound = mixer.Sound('Assets/gameover.wav')


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
    pygame.draw.rect(windowSurface, BLUE, P2)
    pygame.draw.rect(windowSurface, BLUE, P3)
    pygame.draw.rect(windowSurface, BLUE, P4)
    drawText('Assets/Health: %s' % (HEALTH), font, windowSurface, 10, 10)
    drawText("Assets/Bonus Score: %s" % (BONUS), font, windowSurface, 10, 45)
    pygame.display.flip()
    windowSurface.fill(WHITE)


def y_trajectory(y_basis, y_speed, t):
    y = y_basis - ((-9.81 / 30) * t ** 2 / 2 + y_speed * t)
    return y


def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, WHITE)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Set up the Start screen of the game:
windowSurface.blit(StartScreen, (0, 0))
StartJingle.play()
pygame.display.update()
time.sleep(5)
waitForPlayerToPressKey()
musicPlaying = True
running = True

while running:

    moveLeft = moveRight = False
    mixer.music.play(-1, 0.0)

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
                        mixer.music.stop()
                    else:
                        mixer.music.play(-1, 0.0)
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
                    y_basis = playerRect.y+10
                elif playerRect.y <= P1_Y:
                    isJump = False
                    playerRect.y = P1_Y-50
                    isOnP1 = True
                if P1_Y+P_Y>playerRect.y>P1_Y-49:
                    isOnP1=False

            if playerRect.colliderect(P2):
                if playerRect.y > P2_Y:
                    y_speed = 0
                    t = 0
                    y_basis = playerRect.y+10
                elif playerRect.y <= P2_Y:
                    isJump = False
                    playerRect.y = P2_Y-50
                    isOnP2 = True
                if P2_Y+P_Y>playerRect.y>P2_Y-49:
                    isOnP2=False

            if playerRect.colliderect(P3):
                if playerRect.y > P3_Y:
                    y_speed = 0
                    t = 0
                    y_basis = playerRect.y+10
                elif playerRect.y <= P3_Y:
                    isJump = False
                    playerRect.y = P3_Y-50
                    isOnP3 = True
                if P3_Y+P_Y>playerRect.y>P3_Y-49:
                    isOnP3=False

            if playerRect.colliderect(P4):
                if playerRect.y > P4_Y:
                    y_speed = 0
                    t = 0
                    y_basis = playerRect.y+10
                elif playerRect.y <= P4_Y:
                    isJump = False
                    playerRect.y = P4_Y-50
                    isOnP4 = True
                if P4_Y+P_Y>playerRect.y>P4_Y-49:
                    isOnP4=False

        if isOnP1 and not(P1_X-25 < playerRect.x < P1_X+P1_LX):
            isOnP1 = False
            isJump = True
            y_speed = 0
            y_basis = playerRect.y
            t = 0

        if isOnP2 and not(P2_X-25 < playerRect.x < P2_X+P2_LX):
            isOnP2 = False
            isJump = True
            y_speed = 0
            y_basis = playerRect.y
            t = 0

        if isOnP3 and not(P3_X-25 < playerRect.x < P3_X+P3_LX):
            isOnP3 = False
            isJump = True
            y_speed = 0
            y_basis = playerRect.y
            t = 0

        if isOnP4 and not(P4_X-25 < playerRect.x < P4_X+P4_LX):
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

        badRect.x += BADDIEMOVERATE
        if badRect.x <= 0:
            badRect.x -= BADDIEMOVERATE
            BADDIEMOVERATE = -BADDIEMOVERATE
        elif badRect.x >= 550:
            badRect.x -= BADDIEMOVERATE
            BADDIEMOVERATE = -BADDIEMOVERATE
        if not(badRect.colliderect(P1) or badRect.colliderect(P2) or badRect.colliderect(P3)) and not badJump:
            bad_y_speed = 0
            badJump = True
            bad_y_basis = badRect.y
            t_bad = 0
        if (badRect.colliderect(P1) or badRect.colliderect(P2) or badRect.colliderect(P3)) and badJump:
            badJump = False

        if badJump:
            badRect.y=y_trajectory(bad_y_basis,bad_y_speed,t_bad)
            t_bad += 1

        if playerRect.colliderect(badRect):
            mixer.music.stop()
            HitSound.play()
            waitForPlayerToPressKey()
            playerRect.update(50, 480, 50, 50)
            badRect.update(500, 480, 50, 50)
            moveLeft = moveRight = False
            HitSound.stop()
            mixer.music.play(-1, 0.0)
            HEALTH -= 1
            playerRect.y = 480
            isOnP1 = False
            BONUS = 5000

        if HEALTH == 0:
            mixer.music.load('Assets/gameover.wav')
            mixer.music.play()
            running = False
            terminate()

        bonus_cpt += 1
        if bonus_cpt > 150:
            BONUS -= 100
            bonus_cpt = 0

        redrawScreen()
        mainClock.tick(FPS)