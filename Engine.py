import pygame

game_over = False
game_won = False

def trigger_game_over():
    global game_over
    game_over = True

def trigger_game_won():
    global game_won, game_over
    game_won = True
    game_over = True

def reset_game():
    global game_over, game_won
    game_over = False
    game_won = False

    """Nettoie et réinitialise le jeu sans relancer la boucle."""
    from Objects import Player, DialogueManager
    from Data import MiniGun, FlameThrower, HealthPotion, SpeedPotion, RegenPotion, Sword
    import SceneManager
    from InventorySystem import CraftingManager

    # Nettoyer la scène
    if SceneManager.Scene.currentScene:
        SceneManager.Scene.currentScene.objects.clear()

    SceneManager.SCENES["center"].load("SpawnPoint")

    Player(
        SceneManager.Scene.currentScene.tilemap.points["SpawnPoint"], 
        pygame.Vector2(15, 17), 
        r"data/Sprites/hero.png",
        [Sword, MiniGun, FlameThrower, HealthPotion, RegenPotion, SpeedPotion],  # Assure-toi que ces imports sont disponibles
        100,
        300
    )

    DialogueManager()

    for recipe in CraftingManager.recipes:
        recipe.isCraftable = True

def get_game_over_buttons(screen):
    width, height = screen.get_size()
    button_w, button_h = 240, 60
    x = width // 2 - button_w // 2
    restart_rect = pygame.Rect(x, height // 2 + 40, button_w, button_h)
    quit_rect = pygame.Rect(x, height // 2 + 120, button_w, button_h)
    return restart_rect, quit_rect


def draw_game_over(screen, message):
    width, height = screen.get_size()
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    font_title = pygame.font.SysFont("Arial", 60, bold=True)
    font_btn = pygame.font.SysFont("Arial", 24, bold=True)

    title_text = font_title.render(message, True, (255, 50, 50))
    title_rect = title_text.get_rect(center=(width // 2, height // 2 - 60))
    screen.blit(title_text, title_rect)

    restart_rect, quit_rect = get_game_over_buttons(screen)

    pygame.draw.rect(screen, (60, 60, 120), restart_rect, border_radius=12)
    pygame.draw.rect(screen, (255, 255, 255), restart_rect, 2, border_radius=12)
    restart_text = font_btn.render("Recommencer", True, (255, 255, 255))
    restart_text_rect = restart_text.get_rect(center=restart_rect.center)
    screen.blit(restart_text, restart_text_rect)

    pygame.draw.rect(screen, (120, 60, 60), quit_rect, border_radius=12)
    pygame.draw.rect(screen, (255, 255, 255), quit_rect, 2, border_radius=12)
    quit_text = font_btn.render("Quitter", True, (255, 255, 255))
    quit_text_rect = quit_text.get_rect(center=quit_rect.center)
    screen.blit(quit_text, quit_text_rect)


def Run (screen: pygame.surface.Surface, DEBUG: bool):
    import SceneManager
    from UI import UIElement

    font = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()
    dt = 0
    running = True

    # Initialisation
    reset_game()

    while running:

        restart_rect, quit_rect = None, None
        if game_over:
            restart_rect, quit_rect = get_game_over_buttons(screen)

        #EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if game_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_rect and restart_rect.collidepoint(event.pos):
                    reset_game()
                elif quit_rect and quit_rect.collidepoint(event.pos):
                    running = False

            if not game_over:
                for obj in SceneManager.Scene.currentScene.objects:
                    obj.HandleEvent(event)

        screen.fill(pygame.Color(0, 0, 0))
            
        if game_won:
            draw_game_over(screen, "GAME WON")
        else:
            if game_over:
                draw_game_over(screen, "GAME OVER")
            else:
            # UPDATE
                for obj in SceneManager.Scene.currentScene.objects:
                    obj.Update(dt)

                # RENDER
                # Objects
                for obj in SceneManager.Scene.currentScene.objects:
                    if not isinstance(obj, UIElement):
                        obj.Render(screen, DEBUG)

                # UI
                for obj in SceneManager.Scene.currentScene.objects:
                    if isinstance(obj, UIElement):
                        obj.Render(screen, DEBUG)


        fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255,255,255))
        screen.blit(fps_text, pygame.Vector2(20, pygame.display.Info().current_h - 75))

        # update the display
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame
        dt = clock.tick(60) / 1000

    pygame.quit()