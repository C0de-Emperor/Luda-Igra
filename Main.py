import pygame
import Engine
pygame.init()
pygame.display.set_caption("Luda Igra")
SCREEN = pygame.display.set_mode((1200, 800))
DEBUG = True

Engine.Run(SCREEN, DEBUG)