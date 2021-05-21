import pygame, sys, time, random
from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()


# CONSTANTS & VARIABLES
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


# ASSETS

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
potion = pygame.image.load("Assets/potion.png")
potionRect = potion.get_rect()
potion_y = {0: P_Y, 1: P1_Y, 2: P2_Y, 3: P3_Y}
potionRect.x = random.randint(0, 600)
potionRect.y = potion_y[random.randint(0, 3)]+30

# Set up music.
StartJingle = pygame.mixer.Sound("Assets/StartJingle.wav")
pygame.mixer.music.load('Assets/background.wav')
HitSound = pygame.mixer.Sound('Assets/hit_sound.wav')
GameOverSound = pygame.mixer.Sound('Assets/gameover.mp3')
TimeRun = pygame.mixer.Sound("Assets/run_time.mp3")
WinSound = pygame.mixer.Sound("Assets/win_sound.mp3")