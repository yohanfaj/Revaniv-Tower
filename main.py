import pygame, sys, time
from pygame.locals import *
from pygame import mixer

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
BONUS = 5000
bonus_cpt = 0
isJump = False

# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Revaniv's Tower - Alpha")
pygame.mouse.set_visible(True)

# Set up the fonts.
font = pygame.font.Font('fette-unz-fraktur.ttf', 30)

# Set up images.
StartScreen = pygame.image.load("main_menu.png")
logo = pygame.image.load('logoicon.ico')
player = pygame.image.load("mario.png")
playerRect = pygame.Rect(50, 500, 50, 50)
baddie = pygame.image.load(("goomba.png"))
badRect = pygame.Rect(500, 500, 50, 50)
plat1 = pygame.Rect(100, 450, 400, 10)
bg = pygame.image.load("map_cantine.jpeg")

# Set up music.
StartJingle = mixer.Sound("StartJingle.wav")
mixer.music.load('background.wav')
HitSound = mixer.Sound('hit_sound.wav')
GameOverSound = mixer.Sound('gameover.wav')


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
    pygame.draw.rect(windowSurface, WHITE, plat1)
    drawText('Health: %s' % (HEALTH), font, windowSurface, 10, 10)
    drawText("Bonus Score: %s" % (BONUS), font, windowSurface, 10, 45)
    pygame.display.flip()
    windowSurface.fill(WHITE)


def y_trajectory(y_basis, y_speed, t):
    y = y_basis - (-9.81 * t ** 2 / 2 + y_speed * t)
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
    badLeft = True
    badRight = False
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
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True

                if event.key == K_SPACE and isJump == False:
                    isJump = True

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
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False

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

        if isJump is True:
            playerRect.y -= PLAYERMOVERATE_Y * 2
            PLAYERMOVERATE_Y -= 1
            if PLAYERMOVERATE_Y < -10:
                isJump = False
                PLAYERMOVERATE_Y = 10

        # if badLeft and badRect.left > 0:
        # badRight = False
        # badRect.left -= BADDIEMOVERATE
        # if badRight and badRect.right < WINDOWWIDTH:
        # badLeft = False
        # badRect.right += BADDIEMOVERATE

        badRect.x -= BADDIEMOVERATE
        if badRect.x <= 0:
            badRect.x = 4
            badRect.x += BADDIEMOVERATE
        elif badRect.x >= 550:
            badRect.x = -4
            badRect -= BADDIEMOVERATE

        # Collision Player - Obstacle
        if playerRect.colliderect(badRect):
            mixer.music.stop()
            HitSound.play()
            waitForPlayerToPressKey()
            playerRect.update(50, 500, 50, 50)
            badRect.update(500, 500, 50, 50)
            HitSound.stop()
            mixer.music.play(-1, 0.0)
            HEALTH -= 1
            BONUS = 5000

        # Collision Player - Platform
        if playerRect.colliderect(plat1):
            playerRect.y = plat1.top
            PLAYERMOVERATE_Y = 0


        if HEALTH == 0:
            mixer.music.load('gameover.wav')
            mixer.music.play()
            running = False
            terminate()

        bonus_cpt += 1
        if bonus_cpt > 150:
            BONUS -= 100
            bonus_cpt = 0

        redrawScreen()
        mainClock.tick(FPS)
