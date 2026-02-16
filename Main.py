from Objects import *
from TilemapManager import Tilemap, Biome
import pygame
from pygame import Vector2

DEBUG = True

# pygame setup
pygame.init()
pygame.display.set_caption("Pypy")
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True
dt = 0

biomeTest=Biome("", ["Donjon"], [])



tm = biomeTest.tilemaps[0] # peut être faire un dict pour find une zone / tilemap par son nom et une methode load zone / biome

Biome.loadBiome(biomeTest, tm, screen)

player = Player(
        Tilemap.currentTilemap.spawn_point, 
        Vector2(50, 50),
        r"player.png",
        speed = 300
    )


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(pygame.Color(0, 0, 0))

    # RENDER & UPDATE
    for obj in Object.instances:
        obj.Update(dt)
        obj.Render(screen, DEBUG)


    # update the display
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()




    
