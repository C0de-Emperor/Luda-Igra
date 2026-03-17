import pygame

class ResourceManager:
    resources = []

    @classmethod
    def register(cls, resource):
        cls.resources.append(resource)

class ItemStack:
    def __init__(self, resource: "Resource", amount: int):
        self.resource = resource
        self.amount = amount

    def add(self, quantity: int):
        space = self.resource.max_stack - self.amount
        added = min(space, quantity)

        self.amount += added
        return quantity - added  # reste

    def remove(self, quantity: int):
        removed = min(self.amount, quantity)
        self.amount -= removed
        return removed

    def is_empty(self):
        return self.amount <= 0

class Inventory:
    slot_size = 50
    padding = 5

    def __init__(self):
        from UI import InventoryUI

        self.resources = {}
        self.UI = InventoryUI(self, pygame.Vector2(0, 0))

    def add(self, resource, amount):
        self.resources[resource] = self.resources.get(resource, 0) + amount

    def remove(self, resource, amount):
        self.resources[resource] = self.resources.get(resource, 0) - amount

    def get(self, resource):
        return self.resources.get(resource, 0)
    
class Resource:
    def __init__(self, name: str, icon: str):
        self.name = name
        self.icon = pygame.image.load(icon).convert_alpha()

        self.icon = pygame.transform.scale(self.icon, (Inventory.slot_size - 10, Inventory.slot_size - 10))

        ResourceManager.register(self)

WOOD = Resource("Wood", r"data/Sprites/log.png")
STONE = Resource("Stone", r"data/Sprites/stone.png")
IRON = Resource("Iron", r"data/Sprites/bullet.png")

