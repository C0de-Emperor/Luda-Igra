import pygame

def Run (screen: pygame.surface.Surface, DEBUG: True):
    from Objects import Player
    import SceneManager

    clock = pygame.time.Clock()
    dt = 0
    running = True

    SceneManager.SCENES["carte"].load("SpawnPoint")

    Player(SceneManager.Scene.currentScene.tilemap.points["SpawnPoint"] , pygame.Vector2(50, 50), r"data/sprites/toruk_makto.png", speed=800)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(pygame.Color(0, 0, 0))

        keys = pygame.key.get_pressed()

        # RENDER & UPDATE
        for obj in SceneManager.Scene.currentScene.objects:
            obj.Update(dt)
            obj.Render(screen, DEBUG)


        # update the display
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()