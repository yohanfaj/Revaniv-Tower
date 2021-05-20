import pygame, sys, random
from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
import constants as cst
import assets as ast

pygame.init()
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))


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
    pygame.draw.rect(windowSurface, cst.BLUE, cst.P1)
    pygame.draw.rect(windowSurface, cst.BLUE, cst.P2)
    pygame.draw.rect(windowSurface, cst.BLUE, cst.P3)
    pygame.draw.rect(windowSurface, cst.BLUE, cst.P4)
    drawText('Health: %s' % cst.HEALTH, ast.font, windowSurface, cst.WHITE, 10, 10)
    drawText("Time Score: %s" % cst.BONUS, ast.font, windowSurface, cst.WHITE, 10, 45)
    pygame.display.flip()
    windowSurface.fill(cst.WHITE)


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
    drawText("%s" % cst.finalscore, ast.font, windowSurface, cst.WHITE, 335, 107.5)
    pygame.display.update()
    waitForPlayerToPressKey()


