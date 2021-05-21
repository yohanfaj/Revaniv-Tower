import pygame, sys, time
from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
import constants as cst

pygame.init()

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
GameOverSound = pygame.mixer.Sound('Assets/gameover.mp3')
TimeRun = pygame.mixer.Sound("Assets/run_time.mp3")
WinSound = pygame.mixer.Sound("Assets/win_sound.mp3")