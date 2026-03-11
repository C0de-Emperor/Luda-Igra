import pygame
import Engine
pygame.init()
pygame.display.set_caption("Luda Igra")
SCREEN = pygame.display.set_mode((1800, 1000))
DEBUG = False

Engine.Run(SCREEN, DEBUG)