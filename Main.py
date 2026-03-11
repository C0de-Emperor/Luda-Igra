import pygame
import Engine
pygame.init()
pygame.display.set_caption("Luda Igra")
SCREEN = pygame.display.set_mode((1900, 1000))
DEBUG = True

Engine.Run(SCREEN, DEBUG)