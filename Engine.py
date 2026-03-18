import pygame

def Run (screen: pygame.surface.Surface, DEBUG: True):
    from Objects import Player, Harvestable
    from Data import RocketLaucher, MiniGun, FlameThrower
    import SceneManager
    from InventorySystem import WOOD, ItemStack


    font = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()
    dt = 0
    running = True

    SceneManager.SCENES["carte"].load("SpawnPoint")

    Player(
        SceneManager.Scene.currentScene.tilemap.points["SpawnPoint"], 
        pygame.Vector2(50, 50), 
        r"data/Sprites/toruk_makto.png",
        [RocketLaucher, MiniGun, FlameThrower],
        speed=800
    )

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            for obj in SceneManager.Scene.currentScene.objects:
                obj.HandleEvent(event)


        screen.fill(pygame.Color(0, 0, 0))

        # RENDER & UPDATE
        for obj in SceneManager.Scene.currentScene.objects:
            obj.Update(dt)
            obj.Render(screen, DEBUG)

        fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255,255,255))
        screen.blit(fps_text, (100,100))

        # update the display
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame
        dt = clock.tick(60) / 1000

    pygame.quit()