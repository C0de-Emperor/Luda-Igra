import pygame
import Engine
pygame.init()
pygame.display.set_caption("Luda Igra")
SCREEN = pygame.display.set_mode()
DEBUG = False

Engine.Run(SCREEN, DEBUG)