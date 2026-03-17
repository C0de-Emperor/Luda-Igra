import pygame
from Objects import Object

class UIElement(Object):
    def __init__(self, position, size, destroyOnLoad = True):
        super().__init__(position, size, destroyOnLoad)

class InventoryUI(UIElement):
    def __init__(self, inventory, position):
        super().__init__(position, pygame.Vector2(10, 10), False)
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