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
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 24, bold=True)

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
        slot_size = Inventory.slot_size
        padding = Inventory.padding

        # --- BACKGROUND PANEL ---
        panel_width = slot_size + 80 + 20 
        panel_height = len(ResourceManager.resources) * (slot_size + padding) + 60
        panel_rect = pygame.Rect(x - 20, y - 40, panel_width, panel_height)
        
        # Shadow
        shadow_rect = panel_rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect, border_radius=15)
        
        # Main panel
        pygame.draw.rect(screen, (30, 30, 50), panel_rect, border_radius=15)
        pygame.draw.rect(screen, (60, 60, 80), panel_rect, border_radius=15, width=3)
        
        # Title
        title_text = self.title_font.render("INVENTAIRE", True, (200, 220, 255))
        title_rect = title_text.get_rect(center=(panel_rect.centerx, y - 15))
        screen.blit(title_text, title_rect)

        for i, resource in enumerate(ResourceManager.resources):
            amount = self.inventory.get(resource)
            slot_y = y + i * (slot_size + padding)

            # Slot background
            slot_rect = pygame.Rect(x, slot_y, slot_size, slot_size)
            pygame.draw.rect(screen, (45, 45, 65), slot_rect, border_radius=8)
            pygame.draw.rect(screen, (80, 80, 100), slot_rect, border_radius=8, width=2)

            # Icon
            icon_rect = resource.icon.get_rect(center=slot_rect.center)
            screen.blit(resource.icon, icon_rect)



            text_color = (255, 255, 255) if amount < 100 else (255, 215, 0)
            text = self.font.render(str(amount), True, text_color)

            text_bg = pygame.Rect(slot_rect.right + 8, slot_y + slot_size//2 - 12, 50, 24)
            pygame.draw.rect(screen, (20, 20, 30), text_bg, border_radius=5)
            pygame.draw.rect(screen, (60, 60, 80), text_bg, border_radius=5, width=1)
                
            text_rect = text.get_rect(center=text_bg.center)
            screen.blit(text, text_rect)


class CraftingUI(UIElement):
    def __init__(self, position):
        super().__init__(position, False)
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 24, bold=True)
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

        # --- BACKGROUND PANEL ---
        panel_width = 420 + 20  # +20 pour la marge droite uniforme
        panel_height = len(CraftingManager.recipes) * slot_h + 60
        panel_rect = pygame.Rect(x - 20, y - 40, panel_width, panel_height)
        
        # Shadow
        shadow_rect = panel_rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(screen, (0, 0, 0, 120), shadow_rect, border_radius=15)
        
        # Main panel
        pygame.draw.rect(screen, (35, 35, 55), panel_rect, border_radius=15)
        pygame.draw.rect(screen, (70, 70, 90), panel_rect, border_radius=15, width=3)
        
        # Title
        title_text = self.title_font.render("CRAFTING", True, (200, 220, 255))
        title_rect = title_text.get_rect(center=(panel_rect.centerx, y - 15))
        screen.blit(title_text, title_rect)

        for (i, recipe) in enumerate(CraftingManager.recipes):
            rect = pygame.Rect(x, y + i * slot_h, 400, 50)

            # Enhanced colors with better contrast
            if recipe.can_craft() and recipe.isCraftable:
                bg_color = (40, 80, 40)
                border_color = (100, 180, 100)
                hover_bg_color = (60, 120, 60)
                hover_border_color = (140, 220, 140)
            else:
                bg_color = (80, 40, 40)
                border_color = (180, 100, 100)
                hover_bg_color = (120, 60, 60)
                hover_border_color = (220, 140, 140)

            # Background
            pygame.draw.rect(screen, bg_color, rect, border_radius=10)
            
            # Border
            pygame.draw.rect(screen, border_color, rect, border_radius=10, width=2)

            # Hover effect
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, hover_bg_color, rect, border_radius=10)
                pygame.draw.rect(screen, hover_border_color, rect, border_radius=10, width=3)

            offset_x = rect.x + 10
            center_y = rect.centery

            # --- INPUTS ---
            for stack in recipe.inputs:
                # Icon background circle
                icon_bg = pygame.Rect(offset_x, center_y - 16, 32, 32)
                pygame.draw.circle(screen, (60, 60, 80), icon_bg.center, 18)
                
                icon_rect = stack.resource.icon.get_rect(center=icon_bg.center)
                screen.blit(stack.resource.icon, icon_rect)

                # Quantity badge
                qty_text = self.font.render(str(stack.amount), True, (255, 255, 255))
                qty_bg = pygame.Rect(icon_rect.right - 8, icon_rect.bottom - 18, 20, 16)
                pygame.draw.rect(screen, (0, 0, 0, 180), qty_bg, border_radius=8)
                qty_rect = qty_text.get_rect(center=qty_bg.center)
                screen.blit(qty_text, qty_rect)

                offset_x += 40

            # --- ARROW ---
            arrow_text = self.font.render("→", True, (220, 220, 220))
            arrow_rect = arrow_text.get_rect(center=(offset_x + 10, center_y))
            screen.blit(arrow_text, arrow_rect)

            offset_x += 30

            # --- OUTPUT ---
            if isinstance(recipe, ItemRecipe):
                # Icon background
                out_bg = pygame.Rect(offset_x, center_y - 16, 32, 32)
                pygame.draw.circle(screen, (80, 80, 100), out_bg.center, 18)
                
                out_icon = pygame.transform.scale(recipe.output.resource.icon, (32, 32))
                out_rect = out_icon.get_rect(center=out_bg.center)
                screen.blit(out_icon, out_rect)

                # Quantity
                qty_text = self.font.render(str(recipe.output.amount), True, (255, 255, 255))
                qty_bg = pygame.Rect(out_rect.right - 8, out_rect.bottom - 18, 20, 16)
                pygame.draw.rect(screen, (0, 0, 0, 180), qty_bg, border_radius=8)
                qty_rect = qty_text.get_rect(center=qty_bg.center)
                screen.blit(qty_text, qty_rect)
                
            elif isinstance(recipe, WeaponRecipe):
                # Weapon icon
                weapon_icon = pygame.image.load(recipe.output.icon).convert_alpha()
                weapon_icon = pygame.transform.scale(weapon_icon, (32, 32))
                
                out_bg = pygame.Rect(offset_x, center_y - 16, 32, 32)
                pygame.draw.circle(screen, (100, 80, 60), out_bg.center, 18)
                
                out_rect = weapon_icon.get_rect(center=out_bg.center)
                screen.blit(weapon_icon, out_rect)

            # --- CLICK HANDLING ---
            if rect.collidepoint(mouse_pos) and click and self.delay == -1:
                recipe.craft()
                self.delay = 0






















