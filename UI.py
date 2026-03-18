import pygame
from Objects import Object

class UIElement(Object):
    def __init__(self, position, destroyOnLoad = True):
        super().__init__(position, pygame.Vector2(0, 0), destroyOnLoad)

class InventoryUI(UIElement):
    def __init__(self, inventory, position):
        super().__init__(position, False)
        self.inventory = inventory
        self.position = position
        self.font = pygame.font.SysFont(None, 24)

        self.show = False

    def HandleEvent(self, event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.show = not self.show
    
    def Render(self, screen: pygame.surface.Surface, debug: bool = False):
        if not self.show:
            return

        from InventorySystem import ResourceManager, Inventory

        x, y = self.position

        for i, resource in enumerate(ResourceManager.resources):

            amount = self.inventory.get(resource)

            rect = pygame.Rect(x, y + i*(Inventory.slot_size + Inventory.padding), Inventory.slot_size, Inventory.slot_size)

            pygame.draw.rect(screen, (70,70,70), rect)
            pygame.draw.rect(screen, (120,120,120), rect, 2)

            icon_rect = resource.icon.get_rect(center=rect.center)
            screen.blit(resource.icon, icon_rect)

            text = self.font.render(str(amount), True, (255,255,255))
            screen.blit(text, (rect.right + 10, rect.centery - 10))

class CraftingUI(UIElement):
    def __init__(self, position):
        super().__init__(position, False)
        self.font = pygame.font.SysFont(None, 24)
        self.show = False

        self.delay = -1

    def HandleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                self.show = not self.show

    def Update(self, dt):
        if self.delay > -1:
            self.delay += dt

            if self.delay >= 0.3:
                self.delay = -1

    def Render(self, screen, debug=False):
        if not self.show:
            return

        from InventorySystem import CraftingManager, ItemRecipe, WeaponRecipe

        x, y = self.position
        slot_h = 60

        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        for (i, recipe) in enumerate(CraftingManager.recipes):

            rect = pygame.Rect(x, y + i * slot_h, 400, 50)

            # couleur selon craftable
            if recipe.can_craft() and recipe.isCraftable:
                color = (60, 120, 60)
            else:
                color = (120, 60, 60)

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (255,255,255), rect, 2)

            offset_x = rect.x + 10
            center_y = rect.centery

            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255,255,0), rect, 2)

            # --- INPUTS ---
            for stack in recipe.inputs:

                icon = stack.resource.icon

                # scale propre si besoin
                icon = pygame.transform.scale(icon, (32, 32))

                icon_rect = icon.get_rect(center=(offset_x + 16, center_y))
                screen.blit(icon, icon_rect)

                # quantité
                txt = self.font.render(str(stack.amount), True, (255,255,255))
                screen.blit(txt, (icon_rect.right - 5, icon_rect.bottom - 15))

                offset_x += 40

            # --- FLECHE ---
            arrow = self.font.render(" =", True, (255,255,255))
            arrow_rect = arrow.get_rect(center=(offset_x + 10, center_y))
            screen.blit(arrow, arrow_rect)

            offset_x += 30

            if isinstance(recipe, ItemRecipe):
                # --- OUTPUT ---
                out_icon = pygame.transform.scale(recipe.output.resource.icon, (32, 32))
                out_rect = out_icon.get_rect(center=(offset_x + 16, center_y))
                screen.blit(out_icon, out_rect)

                txt = self.font.render(str(recipe.output.amount), True, (255,255,255))
                screen.blit(txt, (out_rect.right - 5, out_rect.bottom - 15))
            elif isinstance(recipe, WeaponRecipe):
                a = pygame.image.load(recipe.output.icon).convert_alpha()

                out_icon = pygame.transform.scale(a, (32, 32))
                out_rect = out_icon.get_rect(center=(offset_x + 16, center_y))
                screen.blit(out_icon, out_rect)


            # --- CLICK ---
            if rect.collidepoint(mouse_pos) and click and self.delay == -1:
                recipe.craft()
                self.delay = 0






















