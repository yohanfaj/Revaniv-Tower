import pygame, sys, random
from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
import assets as ast

pygame.init()

# CONSTANTS & VARIABLES:
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

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
    windowSurface.blit(ast.bg, (0, 0))
    windowSurface.blit(ast.player, ast.playerRect)
    windowSurface.blit(ast.baddie, ast.badRect)
    windowSurface.blit(ast.tomato1, ast.tomato1rect)
    windowSurface.blit(ast.tomato2, ast.tomato2rect)
    windowSurface.blit(ast.tomato3, ast.tomato3rect)
    pygame.draw.rect(windowSurface, BLUE, P1)
    pygame.draw.rect(windowSurface, BLUE, P2)
    pygame.draw.rect(windowSurface, BLUE, P3)
    pygame.draw.rect(windowSurface, BLUE, P4)
    drawText('Health: %s' % HEALTH, ast.font, windowSurface, WHITE, 10, 10)
    drawText("Time Score: %s" % BONUS, ast.font, windowSurface, WHITE, 10, 45)
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
    drawText("%s" % finalscore, ast.font, windowSurface, WHITE, 335, 107.5)
    pygame.display.update()
    waitForPlayerToPressKey()


