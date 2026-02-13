

# Example file showing a basic pygame "game loop"
from Objects import *
import pygame
from pygame import Vector2

# pygame setup
pygame.init()
pygame.display.set_caption("Pypy")
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0


player = Player(
    Vector2(screen.get_width() / 2, screen.get_height() / 2), 
    Vector2(50, 230),
    r"player.png",
    speed=600
    )


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(pygame.Color(52, 168, 235))

    # RENDER YOUR GAME HERE
    for obj in Object.instances:
        obj.Update(dt)
        obj.Render(screen)


    # update the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()




    
