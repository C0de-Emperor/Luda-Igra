import math
import pygame
from Objects import Object
from Tools import Queue

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from InventorySystem import Resource, Inventory
    from DialogueSystem import DialogueManager

class UIElement(Object):
    def __init__(self, position, destroyOnLoad = True):
        super().__init__(position, pygame.Vector2(0, 0), destroyOnLoad)


class ItemNotification(UIElement):
    notifications:list = []

    def __init__(self, resource, amount):
        position = pygame.Vector2(30, pygame.display.Info().current_h - 130)
        super().__init__(position, False)
        
        self.resource:Resource = resource
        self.amount:int = amount
        self.lifetime:float = 3.0
        self.max_lifetime:float = 3.0
        self.font:pygame.font.Font = pygame.font.SysFont("Arial", 18, bold=True)
        
        ItemNotification.notifications.append(self)

    @staticmethod
    def get_offset_y(index):
        """Calcule le décalage Y en fonction de l'index dans la pile"""
        return index * 45

    def Update(self, dt):
        self.lifetime -= dt
        
        if self.lifetime <= 0:
            self.Destroy()

    def Render(self, screen, DEBUG):
        notifications = ItemNotification.notifications
        
        try:
            index = notifications.index(self)
        except ValueError:
            return

        base_y = pygame.display.Info().current_h - 130
        self.position = pygame.Vector2(30, base_y - ItemNotification.get_offset_y(index))

        if self.lifetime < 0.5:
            alpha = int(255 * (self.lifetime / 0.5))
        else:
            alpha = 255

        notification_width = 200
        notification_height = 40
        notification_surf = pygame.Surface((notification_width, notification_height), pygame.SRCALPHA)

        bg_color = (30, 30, 50, min(alpha, 200))
        pygame.draw.rect(notification_surf, bg_color, (0, 0, notification_width, notification_height), border_radius=10)
        
        # Bordure
        border_color = (100, 150, 255, alpha)
        pygame.draw.rect(notification_surf, border_color, (0, 0, notification_width, notification_height), 2, border_radius=10)

        # Icône
        icon_scaled = pygame.transform.scale(self.resource.icon, (32, 32))
        icon_scaled.set_alpha(alpha)
        notification_surf.blit(icon_scaled, (8, 4))

        # Texte quantité + nom
        text_color = (255, 255, 255, alpha)
        qty_text = self.font.render(f"x{self.amount}", True, text_color)
        qty_text.set_alpha(alpha)
        notification_surf.blit(qty_text, (45, 6))

        name_font = pygame.font.SysFont("Arial", 14, bold=True)
        name_text = name_font.render(self.resource.name, True, text_color)
        name_text.set_alpha(alpha)
        notification_surf.blit(name_text, (45, 22))

        # Rendu final
        screen.blit(notification_surf, self.position)

    def Destroy(self):
        notifications = ItemNotification.notifications
        try:
            index = notifications.index(self)

            temp_list = []
            for i, notif in enumerate(notifications):
                if i != index:
                    temp_list.append(notif)
            ItemNotification.notifications = temp_list
        except ValueError:
            pass
        
        super().Destroy()


class InventoryUI(UIElement):
    def __init__(self, inventory, position):
        super().__init__(position, False)
        self.inventory:Inventory = inventory
        self.position:pygame.Vector2 = position
        self.font:pygame.font.Font = pygame.font.SysFont("Arial", 20, bold=True)
        self.title_font:pygame.font.Font = pygame.font.SysFont("Arial", 24, bold=True)

        self.show:bool = False

    def HandleEvent(self, event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.show:bool = not self.show
    
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
        self.font:pygame.font.Font = pygame.font.SysFont("Arial", 18, bold=True)
        self.title_font:pygame.font.Font = pygame.font.SysFont("Arial", 24, bold=True)
        self.show:bool = False
        self.slotHeight:int = 60

        self.delay:float = -1

    def get_height(self):
        """Retourne la hauteur totale du panel de crafting"""
        from InventorySystem import CraftingManager
        return len(CraftingManager.recipes) * self.slotHeight + 60

    def HandleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                self.show:bool = not self.show

    def Update(self, dt):
        if self.delay > -1:
            self.delay += dt

            if self.delay >= 0.3:
                self.delay = -1

    def Render(self, screen, debug=False):
        if not self.show:
            return

        from Objects import Potion
        from InventorySystem import CraftingManager, ItemRecipe, WeaponRecipe

        x, y = self.position

        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        # --- BACKGROUND PANEL ---
        panel_width = 420 + 20  # +20 pour la marge droite uniforme
        panel_height = len(CraftingManager.recipes) * self.slotHeight + 60
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
            rect = pygame.Rect(x, y + i * self.slotHeight, 400, 50)

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

                offset_x += 50

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
                
                out_icon = recipe.output.resource.icon
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

                out_bg = pygame.Rect(offset_x, center_y - 16, 32, 32)
                pygame.draw.circle(screen, (100, 80, 60), out_bg.center, 18)

                

                if issubclass(recipe.output, Potion):
                    potion_icon = Potion.tint_surface(Potion.liquid_sprite, recipe.output.effect.color)

                    out_rect = potion_icon.get_rect(center=out_bg.center)
                    screen.blit(potion_icon, out_rect)
                    screen.blit(recipe.output.bottle_sprite, out_rect)
                else:
                    weapon_icon = pygame.image.load(recipe.output.icon).convert_alpha()
                    weapon_icon = pygame.transform.scale(weapon_icon, (32, 32))
                
                    out_rect = weapon_icon.get_rect(center=out_bg.center)
                    screen.blit(weapon_icon, out_rect)

            # --- CLICK HANDLING ---
            if rect.collidepoint(mouse_pos) and click and self.delay == -1:
                recipe.addToQueue()
                self.delay = 0


class CraftingQueueUI(UIElement):
    def __init__(self, position, crafting_ui: CraftingUI):
        super().__init__(position, False)
        self.icon_size:float = 40
        self.spacing:float = 10
        self.crafting_ui:CraftingUI = crafting_ui

    def Render(self, screen, debug=False):
        from Objects import Player

        if Player.player is None:
            return
        
        if not self.crafting_ui.show:
            return

        from Objects import Potion
        from InventorySystem import CraftingManager, ItemRecipe, WeaponRecipe


        base_x, base_y = self.position
        crafting_y = self.crafting_ui.position.y
        crafting_height = self.crafting_ui.get_height()
        y = crafting_y + crafting_height + 10 - self.icon_size

        current_recipe = Player.player.recipeToProcess
        cur_progress = 0.0
        total_time = 1.0
        if current_recipe is not None and current_recipe.duration > 0:
            total_time = current_recipe.duration
            cur_progress = min(1.0, Player.player.recipeProcessTimer / total_time)

        queue_items = [current_recipe] if current_recipe != None else []
        queue_items.extend(CraftingManager.craftingQueue.elements)

        if len(queue_items) > 6:
            queue_items = queue_items[: 6]

        # gauche -> premier
        draw_x = base_x

        for i, recipe in enumerate(queue_items):
            cell = pygame.Rect(draw_x, y, self.icon_size, self.icon_size)
            pygame.draw.rect(screen, (80, 80, 80), cell)

            if isinstance(recipe, ItemRecipe):
                icon = pygame.transform.scale(recipe.output.resource.icon, (self.icon_size, self.icon_size ))

                icon_pos = icon.get_rect(center=cell.center)
                screen.blit(icon, icon_pos)
            elif isinstance(recipe, WeaponRecipe):
                if issubclass(recipe.output, Potion):
                    potion_icon = Potion.tint_surface(Potion.liquid_sprite, recipe.output.effect.color)

                    icon_pos = potion_icon.get_rect(center=cell.center)
                    screen.blit(potion_icon, icon_pos)
                    screen.blit(recipe.output.bottle_sprite, icon_pos)
                else:
                    icon = pygame.image.load(recipe.output.icon).convert_alpha()
                    icon = pygame.transform.scale(icon, (32, 32))
                
                    icon_pos = icon.get_rect(center=cell.center)
                    screen.blit(icon, icon_pos)
            
            
            

            if i == 0 and current_recipe is not None:
                # cercle de progression
                center = cell.center
                radius = self.icon_size // 2 - 2
                progress = cur_progress
                total_points = 60
                filled_points = int(total_points * progress)
                for step in range(filled_points):
                    angle = (step / total_points) * 2 * math.pi
                    x1 = center[0] + int(radius * math.cos(angle))
                    y1 = center[1] + int(radius * math.sin(angle))
                    pygame.draw.circle(screen, (255, 165, 0, 180), (x1, y1), 2)

            draw_x += self.icon_size + self.spacing

        if debug:
            debug_rect = pygame.Rect(base_x, y, len(queue_items) * (self.icon_size + self.spacing), self.icon_size)
            pygame.draw.rect(screen, (255, 0, 0), debug_rect, 1)


class DialogueUI(UIElement):
    def __init__(self, dialogueManager:"DialogueManager", position:pygame.Vector2, dialogueBoxDimensions:pygame.Vector2):
        super().__init__(position, False)
        self.position:pygame.Vector2 = position
        self.font:pygame.font.Font = pygame.font.SysFont("Arial", 20, bold=True)

        self.dialogueManager:"DialogueManager" = dialogueManager
        self.dimensions:pygame.Vector2 = dialogueBoxDimensions

        self.show:bool = False
    
    def Render(self, screen: pygame.surface.Surface, debug: bool = False):
        if not self.show:
            return

        from DialogueSystem import Dialogue

        x, y = self.position
        currentDialogueData = self.dialogueManager.getCurrentDialogueData()

        if not currentDialogueData:
            return
        
        NPCSprite:pygame.surface.Surface = currentDialogueData[0]
        currentDialogueText:str = currentDialogueData[1]

        # --- BACKGROUND PANEL ---
        panel_width = self.dimensions.x
        panel_height = self.dimensions.y
        panel_rect = pygame.Rect(x-20, y-20, panel_width, panel_height)
        
        # Shadow
        shadow_rect = panel_rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect, border_radius=15)
        
        # Main panel
        pygame.draw.rect(screen, (30, 30, 50), panel_rect, border_radius=15)
        pygame.draw.rect(screen, (60, 60, 80), panel_rect, border_radius=15, width=3)
        
        # text
        text = self.font.render(currentDialogueText, True, (200, 220, 255))
        text_rect = text.get_rect(topleft=(panel_rect.left+100, panel_rect.top+20))
        screen.blit(text, text_rect)

        # NPC
        NPCRect=pygame.Rect(x-20, y-20, 0, 0)
        NPCSprite=pygame.transform.scale(NPCSprite, (100, 100*NPCSprite.get_width()/NPCSprite.get_height()))
        screen.blit(NPCSprite, NPCRect)





















