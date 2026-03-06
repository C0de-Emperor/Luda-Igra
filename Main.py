from Objects import *
from SceneManager import Scene
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

from SceneManager import BiomeManager

biomeManager=BiomeManager.biomeManager
biomeManager.loadBiome("defaultBiome")
biomeManager.currentBiome.load(0, screen)

currAnimState=0
doBlackScreenTrans=True
TRANS_TIME=1
def blackScreenTrans():
    global currAnimState

    s=pygame.Surface(screen.get_size())
    s.fill((0,0,0))
    if currAnimState<256: s.set_alpha(int(currAnimState))
    else: s.set_alpha(int(512-currAnimState))
    screen.blit(s, (0,0))
    currAnimState+=512/60/TRANS_TIME

    if currAnimState>=512:
        currAnimState=0
        doBlackScreenTrans=False


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(pygame.Color(0, 0, 0))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_h]:
        biomeManager.currentBiome.load(1, screen)
    if keys[pygame.K_j]:
        biomeManager.currentBiome.load(0, screen)

    # RENDER & UPDATE
    for obj in Scene.currentScene.objects:
        obj.Update(dt)
        obj.Render(screen, DEBUG)

    if doBlackScreenTrans:
        blackScreenTrans()

    # update the display
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()




    
