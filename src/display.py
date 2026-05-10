import os
import pygame
from .constants import size, width, height

pygame.init()

screen = pygame.display.set_mode(size)
surface = pygame.Surface((width, height), pygame.SRCALPHA)
font = pygame.font.SysFont('Comic Sans MS', 40)

_assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets')

rules_img = pygame.image.load(os.path.join(_assets_dir, 'rules.jpeg'))
rules = pygame.transform.scale(rules_img, (width, height))
main_bg = pygame.image.load(os.path.join(_assets_dir, 'main_menu_bg.png'))
dark_bg = pygame.image.load(os.path.join(_assets_dir, 'dark_bg.jpg'))
