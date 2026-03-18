import pygame
from Data import RocketLaucher

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Objects import Weapon

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
        from UI import InventoryUI, CraftingUI

        self.resources = {}
        self.UI = InventoryUI(self, pygame.Vector2(20, 20))
        print(pygame.display.Info().current_w - 500)
        self.craftingUI = CraftingUI(pygame.Vector2(pygame.display.Info().current_w - 400 - 10, 10))

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
IRON = Resource("Iron", r"data/Sprites/iron.png")

class CraftingManager:
    recipes: list["Recipe"] = []

    @classmethod
    def register(cls, recipe):
        cls.recipes.append(recipe)

    @classmethod
    def get_craftable(cls):
        return [r for r in cls.recipes if r.can_craft()]

class Recipe:
    def __init__(self, inputs: list[ItemStack]):
        self.inputs = inputs

        self.isCraftable = True

        CraftingManager.register(self)

    def can_craft(self):
        from Objects import Player

        for stack in self.inputs:
            if Player.player.inventory.get(stack.resource) < stack.amount:
                return False
        return True

    def craft(self):
        pass


class ItemRecipe(Recipe):
    def __init__(self, inputs: list[ItemStack], output: ItemStack):
        super().__init__(inputs)

        self.output = output

    def craft(self):
        from Objects import Player

        if not self.can_craft():
            return False

        # retirer les ressources
        for stack in self.inputs:

            Player.player.inventory.remove(stack.resource, stack.amount)

        # ajouter le résultat
        Player.player.inventory.add(self.output.resource, self.output.amount)

        return True
 
class WeaponRecipe(Recipe):
    def __init__(self, inputs: list[ItemStack], output: type["Weapon"]):
        super().__init__(inputs)

        self.output = output
    
    def craft(self):
        from Objects import Player

        if not self.can_craft() or not self.isCraftable:
            return False

        # retirer les ressources
        for stack in self.inputs:
            Player.player.inventory.remove(stack.resource, stack.amount)

        # ajouter le résultat
        Player.player.tools.enqueue(self.output)

        self.isCraftable = False

        return True

IRON_FROM_WOOD = ItemRecipe([
        ItemStack(WOOD, 24)
    ],
    ItemStack(IRON, 3980)
)

ROCKETLAUNCHER_FROM_IRON = WeaponRecipe([
        ItemStack(IRON, 24)
    ],
    RocketLaucher
)







